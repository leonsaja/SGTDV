from django import forms
from django.core.exceptions import ValidationError

from ..models import DestinoViagem


class DestinoViagemForm(forms.ModelForm):

    class Meta:
        model=DestinoViagem
        fields='__all__'

    def clean_nome(self):
        data = self.cleaned_data["nome"]
        data=data.upper()
        
        qs=DestinoViagem.objects.filter(nome=data)
        if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
        if qs.exists():
                raise ValidationError('Já existe Destino com esse nome cadastrado.')
        
        return data
    


