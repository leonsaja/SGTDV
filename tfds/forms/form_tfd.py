from django import forms
from django.forms import ValidationError, inlineformset_factory
from django_select2 import forms as s2forms

from tfds.models import  ReciboTFD,ProcedimentoSia, CodigoSIA


class RecibcoTFDForm(forms.ModelForm):
   
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )


    class Meta:
        model=ReciboTFD
        fields='__all__'
        widgets = {
            'paciente':s2forms.Select2Widget(),
            'acompanhante':s2forms.Select2Widget(),
        }
    def __init__(self, *args, **kwargs):
             super().__init__(*args, **kwargs)

class ProcedimentoSiaForm(forms.ModelForm):
    
    class Meta:
        
        model=ProcedimentoSia
        fields=('codigosia','qtd_procedimento')

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigosia'].widget.attrs.update({'class':'form-control'})
        self.fields['qtd_procedimento'].widget.attrs.update({'class':'form-control'})
        
class CodigoSiaForm(forms.ModelForm):
    
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
       

ProcedimentoSet=inlineformset_factory(ReciboTFD,ProcedimentoSia,form=ProcedimentoSiaForm,extra=1, min_num=1,validate_min=True)

