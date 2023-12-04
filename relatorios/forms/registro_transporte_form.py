from django import forms
from datetime import datetime, timedelta
from cidadao.models import Cidadao
from django_select2 import forms as s2forms


class RelatorioRegistroTransporteForm(forms.Form):

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
    pacientes=forms.ModelChoiceField(label='Paciente', queryset=Cidadao.objects.select_related('endereco','microarea').all(),
                                         required=False,  widget=s2forms.Select2Widget())
   
    STATUS_CHOICES=(
        ('1','SIM'),
        ('2','NÃO,PACIENTE UTILIZOU RECURSOS PROPRIO'),
        ('3','NÃO,PERDEU A CONSULTA'),
        ('4','NÃO, SEM INFORMAÇÃO')
    )
    TIPO_ATENDIMENTO=(
        ('1','EVENTUAL'),
        ('2','ROTINEIRO'),
    )

    ACOMPANHANTE=(
        ('1','SIM'),
        ('2','NÃO'),
    )

    ATEND_ZONA_RURAL=(
        ('1','SIM'),
        ('2','NÃO'),
    )

    acompanhante=forms.ChoiceField(label='Acompanhante ',required=False, widget=forms.RadioSelect,choices=ACOMPANHANTE)
    atend_zona_rural=forms.ChoiceField(label='Atend. Zona Rural ',required=False, widget=forms.RadioSelect,choices=ATEND_ZONA_RURAL)
    tipo_atendimento=forms.ChoiceField(label='Classficação',required=False, widget=forms.RadioSelect,choices=TIPO_ATENDIMENTO)
    status=forms.ChoiceField(label='Status',required=False, widget=forms.RadioSelect,choices=STATUS_CHOICES) 

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
