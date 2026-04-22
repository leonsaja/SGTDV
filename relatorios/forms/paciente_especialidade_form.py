
from django import forms
from datetime import datetime, timedelta
from especialidades.models import Especialidade,ProcedimentosEspecialidade
from django.core.exceptions import ValidationError
from profissionais.models import Profissional
from estabelecimentos.models import Estabelecimento
from datetime import datetime, timedelta,date


class RelatorioPacienteEspecialidadeForm(forms.Form):
    data_inicial=forms.CharField(label='Data Inicial', required=False,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
       
    )
    data_final= forms.CharField(label='Data Final', required=False,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        )
    
    especialidades=forms.ModelChoiceField(label='Especialidade', queryset=Especialidade.objects.all(),
                                         required=True,widget=forms.Select(attrs={'class': 'form-control'}))
    TIPO_CLASSIFICACAO=(
        ('1','ELETIVO'),
        ('2','PRIORIDADE'),
        ('3','URGÊNCIA'),
    )
    STATUS=(
        ('',''),
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
        ('3','CANCELADO'),
        ('4','AUSENTE'),
        ('5','EM TRATAMENTO'),
        ('6','ALTA'),
        ('7','ACOMPANHAMENTO')

    )
    ORDEM=(
        
        ('1','Nome (A - Z)'),
        ('2','Nome (Z - A)'),
        ('3','Mais Recentes'),
        ('4','Mais Antigos'),
        

    )
    ordenar=forms.ChoiceField(label='Ordenar por ',required=True, widget=forms.Select,choices=ORDEM)
    
    classificacao=forms.ChoiceField(label='Classficação',required=False, widget=forms.RadioSelect,choices=TIPO_CLASSIFICACAO)
    status=forms.ChoiceField(label='Status',required=True, widget=forms.Select,choices=STATUS) 
    profissionais=forms.ModelChoiceField(label='ACS', queryset=Profissional.objects.select_related('estabelecimento').filter(cargo='1'),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    estabelecimento=forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    
    procedimento=forms.ModelChoiceField(label='Procedimento', queryset=ProcedimentosEspecialidade.objects.all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    
    """ def clean_data_inicial(self):
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

        return data"""
        
        
    def clean(self):
    
        cleaned_data = super().clean()
        inicial = cleaned_data.get("data_inicial")
        final = cleaned_data.get("data_final")
        data_atual=date.today().strftime('%Y-%m-%d')

        
        if inicial and not final:
            self.add_error('data_final', 'Campo obrigatório ')

            
        if final and not inicial:
            self.add_error('data_inicial', 'Campo obrigatório ')

        
        if inicial and final:
            
            if inicial > final:
                """ raise forms.ValidationError("Data inicial é maior que data final ") """
                self.add_error('data_inicial', 'Data inicial é maior que Data final ')
            
            if inicial > data_atual:
                self.add_error('data_inicial', 'Data inicial é maior que data atual')

            if final >data_atual:
                self.add_error('data_final', 'Data final é maior que data atual')
