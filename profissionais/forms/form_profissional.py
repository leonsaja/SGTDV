from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from profissionais.models import Endereco, Profissional
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
    telefone1 = forms.CharField(
        label='Celular',widget=forms.TextInput(attrs={'placeholder':"(xx) xxxxx-xxxx"})) 
    
    class Meta:
        model=Profissional
        exclude=('endereco','status',)
        
    
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
        self.fields['dt_nascimento'].widget.attrs.update({'class':'mask-data'}),
        self.fields['telefone'].widget.attrs.update({'class':'mask-telefone'}),


class EnderecoForm(forms.ModelForm):

    cep = forms.CharField(
        label='CEP',widget=forms.TextInput(attrs={'placeholder':"00000-000"}))
    
    class Meta:
        model=Endereco
        fields='__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs.update({'class':'mask-cep'})