from django import forms

from ..models import MicroArea


class MicroAreaForm(forms.ModelForm):
    
    class Meta:
        model=MicroArea
        fields='__all__'