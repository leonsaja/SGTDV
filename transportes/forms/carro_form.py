from django import forms
from django.core.exceptions import ValidationError

from ..models import Carro


class CarroForm(forms.ModelForm):

    class Meta:
        model=Carro
        fields='__all__'

    
    def clean_placa(self):
        data = self.cleaned_data["placa"]
        
        if Carro.objects.filter(placa=data).exists():
            raise ValidationError('Já existe um carro com essa placa.')
        return data
    




