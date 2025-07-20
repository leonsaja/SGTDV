from django import forms
from transportes.models import Carro, RegistroTransporte
from django_select2 import forms as s2forms


class RegistroTransporteForm(forms.ModelForm):
    dt_atendimento = forms.DateField(
        label='Data do Atendimento',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
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
    STATUS_CHOICES=(
      ('1','SIM'),
      ('2','NÃO,PACIENTE UTILIZOU RECURSOS PROPRIO'),
      ('3','NÃO,PERDEU A CONSULTA'),
      ('4','NÃO, SEM INFORMAÇÃO')
   )
    status=forms.ChoiceField(label='Transporte Atendido', widget=forms.RadioSelect,choices=STATUS_CHOICES)
    atend_zona_rural=forms.ChoiceField(label='Atend. Zona Rural', widget=forms.RadioSelect,choices=ATEND_ZONA_RURAL)
    acompanhante=forms.ChoiceField(label='Tem Acompanhante', widget=forms.RadioSelect,choices=ACOMPANHANTE)
    tipo_atend=forms.ChoiceField(label='Tipo de Atendimento', widget=forms.RadioSelect,choices=TIPO_ATENDIMENTO)
    
    class Meta:
        model=RegistroTransporte
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget,
            'carro':s2forms.Select2Widget(),
           
        }
        
    def clean(self):
        paciente = self.cleaned_data.get('paciente')
        data = self.cleaned_data.get('dt_atendimento')

        if paciente and data:
            qs = RegistroTransporte.objects.select_related('paciente','carro').filter(paciente=paciente, dt_atendimento=data)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
          
            if qs.exists():
                self.add_error('paciente','Existe registro transporte com paciente com mesma data de atendimento.')
        
        return self.cleaned_data
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        carros=Carro.objects.filter(status=1)
        self.fields['carro'].queryset = carros

"""paciente = self.cleaned_data.get('paciente')
        data=self.cleaned_data.get('dt_atendimento')

        if paciente and data:
            objeto = RegistroTransporte.objects.select_related('paciente','carro').filter(paciente=paciente, dt_atendimento=data).exists()

            if objeto:
                self.add_error('paciente','Existe registro transporte com paciente com mesma data de atendimento. ')
                """