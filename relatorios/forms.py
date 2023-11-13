
from typing import Any
from django import forms

from django.core.exceptions import ValidationError

class RelatorioForm(forms.Form):
    data_inicial=forms.CharField(label='Data Inicial', required=True,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
       
    )
    data_final= forms.CharField(label='Data Final', required=True,widget=forms.DateInput(format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        )
    

    def clean_data_inicial(self):
       data = self.cleaned_data["data_inicial"]
       if not data:
           raise ValidationError('Por favor, digite uma data inicial.')
       return data
    

    def clean_data_final(self):
       data = self.cleaned_data["data_final"]
       
       if not data:
           raise ValidationError('Por favor, digite uma data final.')
       return data
   

        
    def clean(self):

        cleaned_data = super().clean()
        inicial = cleaned_data.get("data_inicial")
        final = cleaned_data.get("data_final")
                                   
        if inicial and final:
            if inicial > final:
                """ raise forms.ValidationError("Data inicial é maior que data final ") """
                self.add_error('data_inicial', 'Data inicial é maior que Data final ')
        
       