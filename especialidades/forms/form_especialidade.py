from django import forms
from django.core.exceptions import ValidationError

from especialidades.models import Especialidade


class EspecialidadeForm(forms.ModelForm):

    class Meta:
        model=Especialidade
        fields='__all__'

   

