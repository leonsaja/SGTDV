from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from ..models import Diaria, Reembolso

class DescricaoReembolsoForm(forms.ModelForm):
    descricao_reembolso=forms.CharField(label='Descrição', widget=forms.Textarea( attrs={'placeholder':'Digite a descrição da Reemboso...','rows':3,'cols':10}))

    class Meta:
        model=Diaria
        fields=['descricao_reembolso']


class ReembolsoForm(forms.ModelForm):


    class Meta:
        model=Reembolso
        fields=['descricao','valor_desp','movimentacao','valor_mov']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'class':'form-select'})
        self.fields['movimentacao'].widget.attrs.update({'class':'form-select'})
        self.fields['valor_desp'].widget.attrs.update({'class':'form-control'})
        self.fields['valor_mov'].widget.attrs.update({'class':'form-control'})

ReembolFormSet=inlineformset_factory(Diaria,Reembolso,form=ReembolsoForm, extra=1)
