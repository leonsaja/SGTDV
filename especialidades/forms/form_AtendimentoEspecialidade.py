from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms
from especialidades.models import AtendimentoEspecialidade,AtendPaciente

class AtendEspecialidadeForm(forms.ModelForm):
    
    class Meta:
        model=AtendimentoEspecialidade
        fields=('data',)
       
        
        
class AtendPacienteForm(forms.ModelForm):
    
    class Meta:
        model=AtendPaciente
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pacientespecialidade'].widget.attrs.update({'class':'clPaciente form-control'})   
        

AtendPacienteformset=inlineformset_factory(AtendimentoEspecialidade,AtendPaciente,form=AtendPacienteForm,extra=1, min_num=1,validate_min=True)
