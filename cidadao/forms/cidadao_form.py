from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from utils.django_form import validarCNS, validarCpf

from ..models import Cidadao, Endereco


class CidadaoForm(forms.ModelForm):
    
    class Meta:
        model=Cidadao
        exclude=('endereco',)
       
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
        self.fields['dt_nascimento'].widget.attrs.update({'class':'mask-data'})
        self.fields['telefone'].widget.attrs.update({'class':'mask-telefone'})
        self.fields['telefone1'].widget.attrs.update({'class':'mask-celular'})
               
class EnderecoForm(forms.ModelForm):
    
    class Meta:
        model=Endereco
        fields='__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cep'].widget.attrs.update({'class':'mask-cep'})
       