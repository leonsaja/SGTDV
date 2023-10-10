from django import forms
from transportes.models import RegistroTransporte


class RegistroTransporteForm(forms.ModelForm):
    dt_atendimento = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    class Meta:
        model=RegistroTransporte
        fields='__all__'
        