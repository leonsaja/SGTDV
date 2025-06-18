
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade


class AtendimentoEspecialidadeForm(forms.ModelForm):

    data_hora_atendimento = forms.DateTimeField(
        label='Data/Hora',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
            }),
        input_formats=('%Y-%m-%dT%H:%M',)
    )
   
    
    class Meta:
        
        model=AtendimentoEspecialidade
        fields='__all__'

   
    
   


       