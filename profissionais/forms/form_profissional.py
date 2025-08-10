from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from profissionais.models import Profissional
from utils.django_form import validarCNS, validarCpf


class ProfissionalForm(forms.ModelForm):
    
    dt_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    telefone = forms.CharField(
        label='Telefone',widget=forms.TextInput(attrs={'placeholder':"(xx) xxxxx-xxxx"}))
   
    
    class Meta:
        model=Profissional
        exclude=('endereco','status',)
        
    def clean_dt_nascimento(self):
        data = self.cleaned_data['dt_nascimento']

        if data > date.today():
            raise ValidationError("A Data de Nascimento não pode ser futura.")
        return data
    
    def clean_cns(self):
        data_cnes=self.cleaned_data.get('cns')
       
        if validarCNS(data_cnes):
            return data_cnes    
        raise ValidationError('Por favor, digite CNS corretamente com 15 digitos. ')
    
    def clean_cpf(self):
        data_cpf=self.cleaned_data.get('cpf')
        
        if data_cpf:
            data=validarCpf(data_cpf)
            if data:
                 return data
        raise  ValidationError('Por favor, digite o CPF corretamente com 15 digitos. ')
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'}),
        self.fields['telefone'].widget.attrs.update({'class':'mask-telefone'}),

