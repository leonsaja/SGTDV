from decimal import Decimal
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms
from dal import autocomplete
from datetime import date, timedelta

from utils.django_form import validarCNS

from ..models import ReciboPassagemTFD


class ReciboPassagemTFDForm(forms.ModelForm):
    ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
     )

    data_recibo = forms.DateField(label='Data',widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date',}),input_formats=('%Y-%m-%d',),)
    valor_paciente_sia=forms.CharField(label='Valor',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':'money'}))
    valor_acompanhante_sia=forms.CharField(label='Valor',required=False, widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':'money'}))
    tem_acompanhante=forms.ChoiceField(label='Tem Acompanhante', widget=forms.RadioSelect,choices=ACOMPANHANTE)
    obs=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

    class Meta:
        model=ReciboPassagemTFD
        fields='__all__'
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
            'acompanhante':autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
        }  

    def clean_codigo_sia_paciente(self):
        data = self.cleaned_data["codigo_sia_paciente"]
        if data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')
    
    
                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def clean_valor_paciente_sia(self):
        data = self.cleaned_data["valor_paciente_sia"]
        return Decimal(data.replace(',', '.'))

    def clean_valor_acompanhante_sia(self):
        data = self.cleaned_data["valor_acompanhante_sia"]
        if data:
            return Decimal(data.replace(',', '.'))
        return Decimal(0.00)
    
    def clean_codigo_sia_acompanhante(self):
        data = self.cleaned_data["codigo_sia_acompanhante"]

        if not data:
              return data
          
        elif data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')
    
    def clean(self):
        cleaned_data = super().clean()
        tem_acompanhante=cleaned_data.get('tem_acompanhante')
        quant_passagem_paciente=cleaned_data.get('quant_passagem_paciente')
        acompanhante=cleaned_data.get('acompanhante')
        data_recibo=cleaned_data.get('data_recibo')
        paciente=cleaned_data.get('paciente')
        hoje=date.today()
        limite_minimo=hoje-timedelta(days=1)
        status=cleaned_data.get('status')
        obs=cleaned_data.get('obs')
        
        if status=='3' and not obs:
            self.add_error('obs','Este campo é obrigatório. Por favor, informar motivo do cancelamento do Recibo de passagens')

        qs=ReciboPassagemTFD.objects.select_related('paciente','acompanhante').filter(paciente=paciente, data_recibo=data_recibo)

        if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
        if qs.exists():
            self.add_error('paciente','Este paciente já possui um recibo passagem com essa data.')

        if data_recibo:
            if  data_recibo < limite_minimo:
                if not self.instance.pk:
                    self.add_error(
                        f"data_recibo","A data do recibo não pode ser anterior a 1 dias atrás."
                    )


        if tem_acompanhante == '1':
            acompanhante=cleaned_data.get('acompanhante')
            codigo_sia_acompanhante=cleaned_data.get('codigo_sia_acompanhante')
            valor_acompanhante_sia=cleaned_data.get('valor_acompanhante_sia')
            quant_passagem_acompanhante=cleaned_data.get('quant_passagem_acompanhante')
            valor_paciente_sia=cleaned_data.get("valor_paciente_sia")
    
            if not acompanhante:
                 self.add_error('acompanhante', 'Este campo é obrigatório.')

            
            if not codigo_sia_acompanhante:
                  self.add_error('codigo_sia_acompanhante', 'Este campo é obrigatório.')
            
            if not valor_acompanhante_sia:
                  self.add_error('valor_acompanhante_sia', 'Este campo é obrigatório.')

            if not quant_passagem_acompanhante:
                  self.add_error('quant_passagem_acompanhante', 'Este campo é obrigatório.')
            
            if quant_passagem_paciente != quant_passagem_acompanhante:
                self.add_error('quant_passagem_acompanhante', 'Qta devem ser igual entre paciente e acompanhante.')
            if valor_acompanhante_sia != valor_paciente_sia:
                self.add_error('valor_acompanhante_sia', 'Valor devem ser igual entre paciente e acompanhante.')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
