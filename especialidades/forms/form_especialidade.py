from django import forms
from especialidades.models import Especialidade

class EspecialidadeForm(forms.ModelForm):

    class Meta:
        model= Especialidade
        fields='__all__'
