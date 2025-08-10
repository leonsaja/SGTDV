
from django import forms
from datetime import datetime, timedelta
from especialidades.models import Especialidade
from django.core.exceptions import ValidationError


class RelatorioEspecialidadeForm(forms.Form):
    """ data_inicial=forms.CharField(label='Data Inicial',widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
       
    )
    data_final= forms.CharField(label='Data Final',widget=forms.DateInput(format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        )
     """
    especialidades=forms.ModelChoiceField(label='Especialidade', queryset=Especialidade.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
   
    
    