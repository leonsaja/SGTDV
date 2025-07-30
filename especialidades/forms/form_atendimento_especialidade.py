
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade
from django.utils import timezone
from datetime import date

class AtendimentoEspecialidadeForm(forms.ModelForm):

    data = forms.DateTimeField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

   
    class Meta:
        
        model=AtendimentoEspecialidade
        fields='__all__'

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs.update({'class':'mask-hora'})
      
  
  

 

       