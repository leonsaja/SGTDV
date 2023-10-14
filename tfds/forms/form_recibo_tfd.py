from decimal import Decimal
from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms

from tfds.models import  ReciboTFD


class ReciboTFDForm(forms.ModelForm):
   
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )

    class Meta:
        model=ReciboTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
        }
    def __init__(self, *args, **kwargs):
             super().__init__(*args, **kwargs)

