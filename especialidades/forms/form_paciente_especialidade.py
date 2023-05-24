from django import forms
from django_select2 import forms as s2forms

from especialidades.models import PacienteEspecialidade


class PacienteEspecialidadeForm(forms.ModelForm):

    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
    class Meta:
        model= PacienteEspecialidade
        exclude=('especialidade',)
        widgets = {
            'profissional':s2forms.Select2Widget(),
            'paciente':s2forms.Select2Widget(),
           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_pedido'].widget.attrs.update({'class':'mask-data'})

    
