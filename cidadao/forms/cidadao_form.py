from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from utils.django_form import validarCNS, validarCpf

from ..models import Cidadao, Endereco


class CidadaoForm(forms.ModelForm):
    dt_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
   
    
    class Meta:
        model=Cidadao
        exclude=('endereco',)

    def clean_nome_completo(self):
        data=self.cleaned_data.get('nome_completo')
        data=data.upper()
        return data
       
    def clean_cpf(self):
        data_cpf=self.cleaned_data.get('cpf')
        if data_cpf:
            data=validarCpf(data_cpf)
            if data:
                return data
            else:
                raise ValidationError('Por favor, digita o  CPF corretamente com 11 digitos.')
        return data_cpf
        
    def clean_cns(self):
        data_cnes=self.cleaned_data.get('cns')
        
        if validarCNS(data_cnes):
            return data_cnes    
        raise ValidationError('Digite o cartão do SUS com 15 digitos')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'})
        self.fields['telefone'].widget.attrs.update({'class':'mask-telefone'})
        self.fields['telefone1'].widget.attrs.update({'class':'mask-telefone'})
        if self.instance.cpf:
            self.fields['cpf'].widget.attrs['readonly'] = True
               
class EnderecoForm(forms.ModelForm):
    cep = forms.CharField(
        label='CEP',widget=forms.TextInput(attrs={'placeholder':"00000-000"}))
        
    class Meta:
        model=Endereco
        fields='__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cep'].widget.attrs.update({'class':'mask-cep'})
       