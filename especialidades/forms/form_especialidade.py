from django import forms
from django.core.exceptions import ValidationError

from especialidades.models import Especialidade


class EspecialidadeForm(forms.ModelForm):

    class Meta:
        model=Especialidade
        fields='__all__'

    
    def clean_nome(self):
        data = self.cleaned_data["nome"]
        data=data.upper()
        
        qs=Especialidade.objects.filter(nome=data)
        if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
        if qs.exists():
                raise ValidationError('Já existe especialidade com esse nome cadastrado')
        
        return data
    

   

