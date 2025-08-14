from django import forms
from django.forms import inlineformset_factory
from cidadao.models import Cidadao

from especialidades.models import AtendimentoEspecialidade,PacienteSia

class PacienteSiaForm(forms.ModelForm):
     
    
     
     class Meta:
        
        model=PacienteSia
        fields=('hora','paciente',)
        error_messages = {
            'unique_together': "O paciente já foi adicionado a este atendimento."
        }

   
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['hora'].widget.attrs.update({'class':'form-control'})

        
        

AtendPacienteSet=inlineformset_factory(AtendimentoEspecialidade,PacienteSia,form=PacienteSiaForm,extra=1, min_num=1,validate_min=True)
