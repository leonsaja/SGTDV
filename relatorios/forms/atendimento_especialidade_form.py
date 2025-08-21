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
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
        ('3','CANCELADO'),
        

    )

    especialidade=forms.ModelChoiceField(label='Especialidade', queryset=Especialidade.objects.all(),required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    atendimento_via=forms.ChoiceField(label='Classficação',required=True,widget=forms.RadioSelect,choices=ATEND_VIA)
    status=forms.ChoiceField(label='Status',required=True, widget=forms.RadioSelect,choices=STATUS)


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