from django import forms

from ..models import MicroArea
from profissionais.models import Profissional

class MicroAreaForm(forms.ModelForm):
    
    class Meta:
        model=MicroArea
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        acs = Profissional.objects.select_related('estabelecimento').filter(cargo=1)
        self.fields['profissional'].queryset = acs