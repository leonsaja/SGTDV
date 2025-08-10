from django import forms
from django.core.exceptions import ValidationError

from especialidades.models import ProcedimentosEspecialidade


class ProcedEspecialidadeForm(forms.ModelForm):

    class Meta:
        model=ProcedimentosEspecialidade
        fields='__all__'

    
    def clean_nome_procedimento(self):
        data = self.cleaned_data["nome_procedimento"]
        data=data.upper()
        
        if ProcedimentosEspecialidade.objects.filter(nome_procedimento=data).exists():
            raise ValidationError('Já existe procedimento com esse nome cadastrado')
        return data
    

   

