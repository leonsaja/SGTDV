from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from ..models import Diaria, Reembolso


class ReembolsoForm(forms.ModelForm):


    class Meta:
        model=Reembolso
        fields=['descricao','valor_desp','movimentacao','valor_mov']


    def clean_valor_desp(self):
        data=self.cleaned_data['valor_desp']
        print('valor',data)
        return data
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'class':'form-select'})
        self.fields['movimentacao'].widget.attrs.update({'class':'form-select'})
        self.fields['valor_desp'].widget.attrs.update({'class':'form-control'})
        self.fields['valor_mov'].widget.attrs.update({'class':'form-control'})

ReembolFormSet=inlineformset_factory(Diaria,Reembolso,form=ReembolsoForm, extra=1)
