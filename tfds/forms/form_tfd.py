from django import forms
from django.forms import (NumberInput, Textarea, TextInput, ValidationError,
                          inlineformset_factory)
from django_select2 import forms as s2forms

from tfds.models import CodigoSIA, ReciboTFD


class TFDForm(forms.ModelForm):
   
   class Meta:
        model=ReciboTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
                
        }
   def __init__(self, *args, **kwargs):
             super().__init__(*args, **kwargs)
             self.fields['data'].widget.attrs.update({'class':'mask-data'})
        
class CodigoSIAForm(forms.ModelForm):
    
    class Meta:
        
        model=CodigoSIA
        fields='__all__'

    def clean_codigo(self):
        data = self.cleaned_data["codigo"]
        if data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs.update({'class':'form-control'})
        self.fields['valor_unitario'].widget.attrs.update({'class':'form-control'})
        self.fields['qtd_procedimento'].widget.attrs.update({'class':'form-control'})
        self.fields['valor_total'].widget.attrs.update({'class':'form-control'})
    

    
       
CodigoSIASet=inlineformset_factory(ReciboTFD,CodigoSIA,form=CodigoSIAForm,extra=1, min_num=1,validate_min=True)

""" widgets={
    'codigo':NumberInput(attrs={'class':'form-control'}),
    'valor_unitario':NumberInput(attrs={'class':'form-control'}),
    'qtd_procedimento':NumberInput(attrs={'class':'form-control'}),
    'valor_total':NumberInput(attrs={'class':'form-control'}),


} """