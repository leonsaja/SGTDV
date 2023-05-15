from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from ..models import Diaria


class DiariaForm(forms.ModelForm):

    descricao=forms.CharField(label='Descrição', widget=forms.Textarea( attrs={'placeholder':'Digite a descrição da viagem','rows':3,'cols':10}))
    obs=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

    class Meta:
        model=Diaria
        fields='__all__'
        widgets = {
            'profissional':s2forms.Select2Widget(),
           
        }
    def clean_qta_diaria(self):
        data = self.cleaned_data["qta_diaria"]
        if data==0:
            raise ValidationError('Digite um numero acima de 0')
        
        return data
    
    
    def clean_conta(self):
        data_conta=str(self.cleaned_data.get('conta'))
        
        if data_conta:
            if len(data_conta)<=8:
                return data_conta   
            raise ValidationError('Digite a conta corretamente com até 8 digitos.')
        return data_conta
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_diaria'].widget.attrs.update({'class':'mask-data'})
        self.fields['valor'].widget.attrs.update({'class':'mask-money'})





    

