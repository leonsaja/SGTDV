from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms
from especialidades.models import AtendimentoEspecialidade,AtendPaciente

class AtendEspecialidadeForm(forms.ModelForm):
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    
    class Meta:
        model=AtendimentoEspecialidade
        fields='__all__'
               
class AtendPacienteForm(forms.ModelForm):
    
    class Meta:
        model=AtendPaciente
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pacientespecialidade'].widget.attrs.update({'class':'form form-control'})
        
        

AtendPacienteformset=inlineformset_factory(AtendimentoEspecialidade,AtendPaciente,form=AtendPacienteForm,extra=1)
