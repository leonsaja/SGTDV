from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from utils.django_form import validarCpf


class CadastroUsuarioForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ['nome_completo', 'email','cpf','password1', 'password2','dt_nascimento','tipo_usuario',]

    def clean_cpf(self):
      
        data_cpf=self.cleaned_data.get('cpf')
      
        if data_cpf:
            data=validarCpf(data_cpf)
            if len(data)==11:
                return data
        
        raise ValidationError('Por favor, digita o  CPF corretamente com 11 digitos.')
     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'})
        self.fields['dt_nascimento'].widget.attrs.update({'class':'mask-data'})

class EditarUsuarioForm(UserChangeForm):
  
   class Meta:
        model=get_user_model()
        fields = ['nome_completo','email','cpf','dt_nascimento','tipo_usuario','is_active']


   def clean_cpf(self):
       
        data_cpf=self.cleaned_data.get('cpf')
        if data_cpf:
            data=validarCpf(data_cpf)
            
            if data:
                return data
        
        raise ValidationError('Por favor, digita o  CPF corretamente com 11 digitos.')
    
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf'})
     
        self.fields['dt_nascimento'].widget.attrs.update({'class':'mask-data'})
