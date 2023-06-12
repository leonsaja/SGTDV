from django import forms
from django_select2 import forms as s2forms

from ..models import ReciboPassagemTFD


class ReciboPassagemTFDForm(forms.ModelForm):

    codigo_sia_paciente=forms.CharField(label='Código Sia', widget=forms.TextInput())
    class Meta:
        model=ReciboPassagemTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
           
        }
