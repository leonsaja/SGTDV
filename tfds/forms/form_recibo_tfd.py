from decimal import Decimal
from typing import Any
from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms

from tfds.models import  ReciboTFD
from utils.django_form import validarCNS


class ReciboTFDForm(forms.ModelForm):
    ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
     )
    
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    tem_acompanhante=forms.ChoiceField(label='Tem Acompanhante', widget=forms.RadioSelect,choices=ACOMPANHANTE)

    class Meta:
        model=ReciboTFD
        exclude=('status','aprovado_por',)
        widgets = {
            'paciente':s2forms.Select2Widget(),
           
        }
    def clean_cns(self):
        data=self.cleaned_data.get('cns')
        if data:
            if validarCNS(data):
                return data    
            raise ValidationError('Digite o cartão do SUS com 15 digitos')
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        tem_acompanhante=cleaned_data.get('tem_acompanhante')
    
        if tem_acompanhante == '1':
            acompanhante=cleaned_data.get('acompanhante')
            rg=cleaned_data.get('rg')
            cpf=cleaned_data.get('cpf')
            cns=cleaned_data.get('cns')
            
            if not acompanhante:
                 self.add_error('acompanhante', 'Este campo é obrigatório.')

            if not rg:
                 self.add_error('rg', 'Este campo é obrigatório.')
            
            if not cpf:
                 self.add_error('cpf', 'Este campo é obrigatório.')

            if not cns:
                 self.add_error('cns', 'Este campo é obrigatório.')
            

           
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'})

class ReciboTFDStatusForm(forms.ModelForm):
    
    class Meta:
        model=ReciboTFD
        fields=['status']
        