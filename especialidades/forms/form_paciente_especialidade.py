from datetime import date
from django import forms
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from especialidades.models import PacienteEspecialidade
from cidadao.models import Cidadao
from dal import autocomplete

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
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
            'procedimento':s2forms.Select2Widget(),
           
        }
    def clean_data_pedido(self):
        data = self.cleaned_data['data_pedido']
                
        if data > date.today():
            raise ValidationError("A Data do pedido não pode ser futura.")
        return data
    
    def clean(self):
        procedimento = self.cleaned_data.get('procedimento')
        obs=self.cleaned_data.get('observacao')

        if procedimento.nome_procedimento=='EXAMES':
            if not obs:
                self.add_error('observacao', 'Este campo é obrigatório. Por favor, informar quais exames o paciente vai fazer ')

   
           
        
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
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
            'procedimento':s2forms.Select2Widget(),
        }
    
    
    def clean(self):
        paciente = self.cleaned_data.get('paciente')
        procedimento = self.cleaned_data.get('procedimento')
        status = self.cleaned_data.get('status')
        data=self.cleaned_data.get('data_pedido')


        if paciente and procedimento and status and data:
            qs = PacienteEspecialidade.objects.select_related('paciente','procedimento','especialidade').filter(paciente=paciente,procedimento=procedimento,status=status,data_pedido=data)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('paciente','Este paciente já possui um cadastro  nessa especialidade com mesmo procedimento, status e data.')
           
           
"""
 form.instance.especialidade = get_object_or_404(Especialidade, id=self.kwargs.get('id'))
        return super().form_valid(form)"""