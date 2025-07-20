from typing import Any
from django import forms
from datetime import datetime, timedelta,date
from especialidades.models import Especialidade,ProcedimentosEspecialidade
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
    ATEND_VIA=(

            ('1','CIMBAJE'),
            ('2','CEAE'),
            ('3','RECURSO PRÓPRIO'),
            ('4','PPI'),

        )

    especialidade=forms.ModelChoiceField(label='Especialidade', queryset=Especialidade.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    atendimento_via=forms.ChoiceField(label='Classficação',required=False, widget=forms.Select,choices=ATEND_VIA)
