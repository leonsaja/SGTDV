from decimal import Decimal
from typing import Any
from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms
from datetime import date, timedelta
from tfds.models import  ReciboTFD
from utils.django_form import validarCNS
from dal import autocomplete


class ReciboTFDForm(forms.ModelForm):
    ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
     )
    PAGAMENTO_POR=(
      ('1','PIX'),
      ('2','CONTA'),
      
   )
    FORA_ESTADO=(
     ('1','SIM'),
     ('2','NÃO'),
   )
    
    data = forms.DateField(
        label='Data do Atendimento',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    tem_acompanhante=tem_acompanhante=forms.ChoiceField(label='Tem Acompanhante', widget=forms.RadioSelect,choices=ACOMPANHANTE)
    pagamento_por=forms.ChoiceField(label='PAGAMENTO POR', widget=forms.RadioSelect,choices=PAGAMENTO_POR)
    atend_fora_estado=forms.ChoiceField(label='ATENDIMENTO FORA DO ESTADO', widget=forms.RadioSelect,choices=FORA_ESTADO)

    class Meta:
        model=ReciboTFD
        exclude=('status','aprovado_por','criado_por','alterado_por')
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
            'acompanhante':autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
        }

    def clean_cns(self):
        cns=self.cleaned_data.get('cns')
        if cns:
            if validarCNS(cns):
                return cns    
            raise ValidationError('Digite o cartão do SUS com 15 digitos')
        return cns
    
    def clean(self):
        cleaned_data = super().clean()
        tem_acompanhante=cleaned_data.get('tem_acompanhante')
        pagamento_por=cleaned_data.get('pagamento_por')
        atend_fora_estado=cleaned_data.get('atend_fora_estado')
        acompanhante=cleaned_data.get('acompanhante')
        data=cleaned_data.get('data')
        paciente=cleaned_data.get('paciente')
        hoje=date.today()
        limite_minimo=hoje-timedelta(days=1)

        pg_fonte=cleaned_data.get('pg_fonte')
        pg_conta=cleaned_data.get('pg_conta')

        print('pg_fonte',pg_fonte)
        print('pg_conta',type(pg_conta))
        
        if pg_fonte and pg_conta:
            
            if pg_fonte=='1':
                if pg_conta != pg_fonte:
                    self.add_error('pg_fonte',f'Fonte deve ser para Conta 11522-3.')
            else:
                if pg_conta != pg_fonte:
                    self.add_error('pg_fonte',f'Fonte deve ser para Conta 14753-2.')
                    
        qs=ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').filter(paciente=paciente, data=data)
        if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            self.add_error('paciente','Este paciente já possui um recibo TFD com essa data.')
        
        if data:
            if data > date.today():
                self.add_error("data",'Data não pode ser futura.')
            if  data < limite_minimo:
                if not self.instance.pk:
                    self.add_error(
                        f"data","A data do recibo não pode ser anterior a 7 dias atrás."
                    )
        
        if tem_acompanhante == '1':
            acompanhante=cleaned_data.get('acompanhante')
            
            if not acompanhante:
                 self.add_error('acompanhante', 'Este campo é obrigatório.')
                 
            if acompanhante and paciente == acompanhante:
                self.add_error(
                'acompanhante',"O acompanhante não pode ser a mesma pessoa que o paciente."
                )

        if  tem_acompanhante =='2':
            acompanhante=''
            
        if pagamento_por =='1':
            pix=cleaned_data.get('pix')

            if not pix:
                 self.add_error('pix', 'Este campo é obrigatório.')

        if pagamento_por == '2':
            agencia=cleaned_data.get('agencia')
            conta=cleaned_data.get('conta')

            if not agencia:
                 self.add_error('agencia', 'Este campo é obrigatório.')

            if not conta:
                 self.add_error('conta', 'Este campo é obrigatório.')

        if atend_fora_estado == '1':
            qta_proced=cleaned_data.get('qta_proced')
            valor_passagem=cleaned_data.get('valor_passagem')
            if not qta_proced:
                  self.add_error('qta_proced', 'Este campo é obrigatório.')
   
            if not valor_passagem:
                self.add_error('valor_passagem', 'Este campo é obrigatório.')
         
         
      
                

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class ReciboTFDStatusForm(forms.ModelForm):
    
    class Meta:
        model=ReciboTFD
        fields=['status']
        