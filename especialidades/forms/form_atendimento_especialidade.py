
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade


class AtendimentoEspecialidadeForm(forms.ModelForm):

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

   
    
   


       