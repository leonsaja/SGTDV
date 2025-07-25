
from django import forms
from datetime import datetime, timedelta
from especialidades.models import Especialidade,ProcedimentosEspecialidade
from django.core.exceptions import ValidationError
from profissionais.models import Profissional


class RelatorioPacienteEspecialidadeForm(forms.Form):
    
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
    
    classificacao=forms.ChoiceField(label='Classficação',required=False, widget=forms.RadioSelect,choices=TIPO_CLASSIFICACAO)
    status=forms.ChoiceField(label='Status',required=False, widget=forms.RadioSelect,choices=STATUS) 
    profissionais=forms.ModelChoiceField(label='ACS', queryset=Profissional.objects.select_related('estabelecimento').filter(cargo='1'),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    
    procedimento=forms.ModelChoiceField(label='Procedimento', queryset=ProcedimentosEspecialidade.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))