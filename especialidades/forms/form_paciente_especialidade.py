from datetime import date
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
            'procedimento':s2forms.Select2Widget(),
           
        }
    def clean_data_pedido(self):
        data = self.cleaned_data['data_pedido']
        if data > date.today():
            raise ValidationError("A Data do pedido não pode ser futura.")
        return data
    
    def clean(self):
        paciente = self.cleaned_data.get('paciente')
        procedimento = self.cleaned_data.get('procedimento')
        status=self.cleaned_data.get('status')
        data_pedido=self.cleaned_data.get('data_pedido')

        if paciente and status:
            qs = PacienteEspecialidade.objects.select_related('paciente','procedimento','especialidade').filter(paciente=paciente, status=status,procedimento=procedimento,data_pedido=data_pedido)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('paciente','Existe Paciente já cadastrado na especialidade com Status: "AGUARDANDO" e com mesmo "PROCEDIMENTO"')

        
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
    
