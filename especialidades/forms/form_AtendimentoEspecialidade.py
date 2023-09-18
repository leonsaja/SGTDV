from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms
from especialidades.models import AtendimentoEspecialidade,PacienteEspecialidade

class AtendEspecialidadeForm(forms.ModelForm):
    
    class Meta:
        model=AtendimentoEspecialidade
        fields=('data',)
       

AtendEspformset=inlineformset_factory(PacienteEspecialidade,AtendimentoEspecialidade,fields=('pacientespecialidade',),extra=1, min_num=1,validate_min=True)
