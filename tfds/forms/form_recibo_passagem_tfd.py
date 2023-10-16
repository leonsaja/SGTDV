from decimal import Decimal
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from ..models import ReciboPassagemTFD


class ReciboPassagemTFDForm(forms.ModelForm):

    data_recibo = forms.DateField(label='Data',widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date',}),input_formats=('%Y-%m-%d',),)
    valor_paciente_sia=forms.CharField(label='Valor',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':'money'}))
    valor_acompanhante_sia=forms.CharField(label='Valor',required=False, widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':'money'}))

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

    
