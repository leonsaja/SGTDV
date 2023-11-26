from django import forms
from datetime import datetime, timedelta
from especialidades.models import Especialidade
from django.core.exceptions import ValidationError
from cidadao.models import Cidadao
from django_select2 import forms as s2forms


class RelatorioReciboTfdsForm(forms.Form):

    data_inicial=forms.CharField(label='Data Inicial',widget=forms.DateInput(
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
    pacientes=forms.ModelChoiceField(label='Paciente', queryset=Cidadao.objects.select_related('endereco','microarea').all(),
                                         required=False,  widget=s2forms.Select2Widget())
    

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
