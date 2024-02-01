
from typing import Any
from django import forms
from datetime import datetime, timedelta,date
from profissionais.models import Profissional
from django.core.exceptions import ValidationError

class RelatorioDiariaForm(forms.Form):
    data_inicial=forms.CharField(label='Data Inicial', required=True,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
       
    )
    data_final= forms.CharField(label='Data Final', required=True,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        )
    
    profissionais=forms.ModelChoiceField(label='Profissional', queryset=Profissional.objects.select_related('estabelecimento','microarea').all(),
                                         required=False,  
    widget=forms.Select(attrs={'class': 'form-control'}))
   
    def clean_data_inicial(self):
        data = self.cleaned_data["data_inicial"]
        data_atual=date.today().strftime('%Y-%m-%d')
        
        if data > data_atual:
            raise ValidationError('Data inicial é maior que data atual')

        return data
    
    def clean_data_final(self):
        data = self.cleaned_data["data_final"]
        data_atual=date.today().strftime('%Y-%m-%d')
        if data > data_atual:
            raise ValidationError('Data final é maior que data atual')

        return data
     
   

        
    def clean(self):

        cleaned_data = super().clean()
        inicial = cleaned_data.get("data_inicial")
        final = cleaned_data.get("data_final")
        
        if inicial and final:
            inicial_data=datetime.strptime(inicial,'%Y-%m-%d')
            final_data=datetime.strptime(final,'%Y-%m-%d')
            
            if inicial > final:
                """ raise forms.ValidationError("Data inicial é maior que data final ") """
                self.add_error('data_inicial', 'Data inicial é maior que Data final ')

            data_limite=timedelta(days=180)
            pesquisado=final_data-inicial_data

            if pesquisado > data_limite:
                self.add_error('data_inicial', 'Periodo maior que 6 meses ')
                self.add_error('data_final', 'Periodo maior que 6 meses ')

        
        
       