from django import forms
from transportes.models import Carro, RegistroTransporte
from django_select2 import forms as s2forms
from datetime import date
from dal import autocomplete


class RegistroTransporteForm(forms.ModelForm):
    dt_atendimento = forms.DateField(
        label='Data do atendimento',
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
    status=forms.ChoiceField(label='Transporte atendido', widget=forms.RadioSelect,choices=STATUS_CHOICES)
  
    class Meta:
        model=RegistroTransporte
        fields='__all__'
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
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
    
    
    def clean_dt_atendimento(self):
        data = self.cleaned_data['dt_atendimento']
        data_atual=date.today().strftime('%Y')
        data_anterior=data.strftime('%Y')
        
        if data > date.today():
            raise forms.ValidationError("A Data de atendimento não pode ser futura.")
    
        if  data_anterior < data_atual:
            raise forms.ValidationError("A data do atendimento não pode ser anterior ao um Ano")
        
        return data
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