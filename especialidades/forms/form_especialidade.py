from django import forms
from django.core.exceptions import ValidationError

from especialidades.models import Especialidade


class EspecialidadeForm(forms.ModelForm):

    class Meta:
        model=Especialidade
        fields='__all__'

    def clean_nome(self):
        data = self.cleaned_data["nome"]

        if Especialidade.objects.filter(nome=data).exists():
            raise ValidationError('Já existe uma especialidade com esse nome.')
        
        return data
    

