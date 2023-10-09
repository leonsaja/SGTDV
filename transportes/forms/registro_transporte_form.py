from django import forms
from transportes.models import RegistroTransporte


class RegistroTransporteForm(forms.ModelForm):
    class Meta:
        model=RegistroTransporte
        fields='__all__'
        