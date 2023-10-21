from decimal import Decimal
from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms

from tfds.models import  ReciboTFD
from utils.django_form import validarCNS


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
           
        }
    def clean_cns(self):
        data=self.cleaned_data.get('cns')
        if data:
            if validarCNS(data):
                return data    
            raise ValidationError('Digite o cartão do SUS com 15 digitos')
        return data
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'})
