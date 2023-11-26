
from django import forms
from datetime import datetime, timedelta
from especialidades.models import Especialidade
from django.core.exceptions import ValidationError
from profissionais.models import Profissional


class RelatorioPacienteEspecialidadeForm(forms.Form):
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
                                         required=True,widget=forms.Select(attrs={'class': 'form-control'}))
    TIPO_CLASSIFICACAO=(
        ('1','NORMAL'),
        ('2','URGÊNCIA'),
    )
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
    )
    TIPO_ATENDIMENTO=(
        ('1','CONSULTA'),
        ('2','RETORNO'),
        ('3','AVALIAÇÃO'),
    )
    tipo_atendimento=forms.ChoiceField(label='Tipo de Atendimento ',required=False, widget=forms.RadioSelect,choices=TIPO_ATENDIMENTO)
    classificacao=forms.ChoiceField(label='Classficação',required=False, widget=forms.RadioSelect,choices=TIPO_CLASSIFICACAO)
    status=forms.ChoiceField(label='Status',required=False, widget=forms.RadioSelect,choices=STATUS) 
    profissionais=forms.ModelChoiceField(label='ACS', queryset=Profissional.objects.select_related('estabelecimento','microarea').filter(cargo='1'),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
