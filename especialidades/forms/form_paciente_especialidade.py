from django import forms
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from especialidades.models import PacienteEspecialidade
from cidadao.models import Cidadao
class PacienteEspecialidadeForm(forms.ModelForm):

    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
    data_pedido = forms.DateField(
        label='Data do Pedido',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    class Meta:
        model= PacienteEspecialidade
        exclude=('especialidade',)
        widgets = {
            'paciente':s2forms.Select2Widget(),
           
        }
    
    
    def clean(self):
        cleaned_data = super().clean()
        paciente = self.cleaned_data.get('paciente')
        status=self.cleaned_data.get('status')

        if paciente and status:
            objeto = PacienteEspecialidade.objects.filter(paciente=paciente, status=status).exists()

            if objeto:
                self.add_error('paciente','Existe Paciente já cadastro na especialidade, com Status: "AGUARDANDO"')

        
class PacienteEspecialidadeUpdateForm(forms.ModelForm):

    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
    data_pedido = forms.DateField(
        label='Data do Pedido',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    class Meta:
        model= PacienteEspecialidade
        exclude=('especialidade',)
        widgets = {
            'paciente':s2forms.Select2Widget(),
           
        }
    
