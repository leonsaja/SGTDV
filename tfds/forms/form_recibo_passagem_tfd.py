from django import forms
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError

from ..models import ReciboPassagemTFD


class ReciboPassagemTFDForm(forms.ModelForm):

    codigo_sia_paciente=forms.CharField(label='Código Sia', widget=forms.TextInput())

    data_recibo = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    valor_paciente_sia = forms.CharField(
        label='Valor',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00"}))

    valor_acompanhante_sia = forms.CharField(
        label='Subtotal',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00"}))

    class Meta:
        model=ReciboPassagemTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
           
        }
    
    def clean_codigo_sia_paciente(self):
        data = self.cleaned_data["codigo_sia_paciente"]
        if data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')
    

    def clean_codigo_sia_acompanhante(self):
        data = self.cleaned_data["codigo_sia_acompanhante"]

        if not data:
              return data
        elif data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')

     
   
        
    

