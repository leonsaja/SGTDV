from decimal import Decimal
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from ..models import ReciboPassagemTFD


class ReciboPassagemTFDForm(forms.ModelForm):

    data_recibo = forms.DateField(label='Data',widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date',}),input_formats=('%Y-%m-%d',),)

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
    

    def clean_codigo_sia_acompanhante(self):
        data = self.cleaned_data["codigo_sia_acompanhante"]

        if not data:
              return data
        elif data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')

    
