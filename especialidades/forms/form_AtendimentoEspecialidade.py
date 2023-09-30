from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms
from especialidades.models import AtendimentoEspecialidade,PacienteEspecialidade, Especialidade

class AtendEspecialidadeForm(forms.ModelForm):
    
    class Meta:
        model=AtendimentoEspecialidade
        fields='__all__'
       

Atendformset=inlineformset_factory(PacienteEspecialidade,AtendimentoEspecialidade,form=AtendEspecialidadeForm,extra=1, min_num=1,validate_min=True)
