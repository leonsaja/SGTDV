from django import forms
from transportes.models import RegistroTransporte


class RegistroTransporteForm(forms.ModelForm):
    dt_atendimento = forms.DateField(
        label='Data de Atendimento',
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
    tipo_atend=forms.ChoiceField(label='Tipo de Atendimento', widget=forms.RadioSelect,choices=TIPO_ATENDIMENTO)
    
    
    class Meta:
        model=RegistroTransporte
        fields='__all__'
        