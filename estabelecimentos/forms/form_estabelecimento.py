from django import forms
from ..models import Estabelecimento
from django.core.exceptions import ValidationError


class EstabelecimentoForm(forms.ModelForm):
    
    class Meta:
        model=Estabelecimento
        fields='__all__'
        
  