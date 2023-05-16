from django import forms

from especialidades.models import  TipoEspecialidade


class TipoEspeciedadesForm(forms.ModelForm):

    class Meta:
        model=TipoEspecialidade
        fields='__all__'



