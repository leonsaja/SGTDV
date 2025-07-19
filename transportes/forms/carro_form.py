from django import forms
from django.core.exceptions import ValidationError

from ..models import Carro


class CarroForm(forms.ModelForm):
    CHOICES_TIPO_TRANSPORTE=(
      ('1','AMBULÂNCIA'),
      ('2','TRANSPORTE SANITÁRIO'),
   )
    CHOICES_FORMA_ATEND=(
      ('1','SERVIÇO PRÓPRIO'),
      ('2','SERVIÇO DO CIS'),
   )
    STATUS=(
        ('1','ATIVO'),
        ('2','DESATIVADO'),
    )
   
    tipo_transporte=forms.ChoiceField(label='Tipo de Transporte', widget=forms.RadioSelect,choices=CHOICES_TIPO_TRANSPORTE)
    forma_atend=forms.ChoiceField(label='Forma de Atendimento', widget=forms.RadioSelect,choices=CHOICES_FORMA_ATEND)
    status=forms.ChoiceField(label='Status', widget=forms.RadioSelect,choices=STATUS)

    class Meta:
        model=Carro
        fields='__all__'

    
  




