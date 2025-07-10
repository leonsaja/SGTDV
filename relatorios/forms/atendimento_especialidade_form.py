from typing import Any
from django import forms
from datetime import datetime, timedelta,date
from especialidades.models import Especialidade
from django.core.exceptions import ValidationError

class RelatorioAtendimentoEspecialidadeForm(forms.Form):
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
    especialidade=forms.ModelChoiceField(label='Especialidade', queryset=Especialidade.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))