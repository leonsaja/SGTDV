from decimal import Decimal
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

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

    class Meta:
        model=ReciboPassagemTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
           
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


        if tem_acompanhante == '1':
            acompanhante=cleaned_data.get('acompanhante')
            codigo_sia_acompanhante=cleaned_data.get('codigo_sia_acompanhante')
            valor_acompanhante_sia=cleaned_data.get('valor_acompanhante_sia')
            quant_passagem_acompanhante=cleaned_data.get('quant_passagem_acompanhante')

    
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
