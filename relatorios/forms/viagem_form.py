from django import forms
from datetime import datetime, timedelta
from cidadao.models import Cidadao
from django_select2 import forms as s2forms

from profissionais.models import Profissional


class RelatorioViagemForm(forms.Form):

    data_inicial=forms.CharField(label='Data Inicial',required=True,widget=forms.DateInput(
        format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
       
    )
    data_final= forms.CharField(label='Data Final',required=True,widget=forms.DateInput(format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        )
    profissionais=forms.ModelChoiceField(label='Motorista', queryset=Profissional.objects.select_related('estabelecimento','microarea').all(),
                                         required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    
    
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
    )

    status=forms.ChoiceField(label='Status',required=False, widget=forms.RadioSelect,choices=STATUS) 

    def clean(self):

        cleaned_data = super().clean()
        inicial = cleaned_data.get("data_inicial")
        final = cleaned_data.get("data_final")
                    
        if inicial and final:
            inicial_data=datetime.strptime(inicial,'%Y-%m-%d')
            final_data=datetime.strptime(final,'%Y-%m-%d')
            
            if inicial > final:
                self.add_error('data_inicial', 'Data inicial é maior que Data final ')

            data_limite=timedelta(days=180)
            pesquisado=final_data-inicial_data

            if pesquisado > data_limite:
                self.add_error('data_inicial', 'Periodo maior que 6 meses ')
                self.add_error('data_final', 'Periodo maior que 6 meses ')
