from django import forms
from django.core.exceptions import ValidationError

from despesas.models import DescricaoReembolso


class DescricaoReembolsoForm(forms.ModelForm):

    class Meta:
        model=DescricaoReembolso
        fields='__all__'

    
    def clean_descricao(self):
        data = self.cleaned_data["descricao"]
                
        if DescricaoReembolso.objects.filter(descricao=data).exists():
            raise ValidationError('Já existe Descricao com esse nome cadastrado')
        
        return data
    

   

