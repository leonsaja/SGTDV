from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from ..models import Diaria, Reembolso

class DescricaoReembolsoForm(forms.ModelForm):
    descricao_reembolso=forms.CharField(label='Descrição', widget=forms.Textarea( attrs={'placeholder':'Digite a descrição da Reemboso...','rows':3,'cols':10}))
    data_ult_nota_reembolso = forms.DateField(label='Data última nota',widget=forms.DateInput( \
        format='%Y-%m-%d',attrs={ 'type': 'date',}),input_formats=('%Y-%m-%d',),help_text='Colocar data da última nota fiscal' )
    class Meta:
        model=Diaria
        fields=['descricao_reembolso','data_ult_nota_reembolso']


class ReembolsoForm(forms.ModelForm):


    class Meta:
        model=Reembolso
        fields=['descricao','valor_desp','obs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'class':'form-select'})
        self.fields['obs'].widget.attrs.update({'class':'form-control'})
        self.fields['valor_desp'].widget.attrs.update({'class':'form-control'})
        


ReembolFormSet=inlineformset_factory(Diaria,Reembolso,form=ReembolsoForm, extra=1, min_num=1,validate_min=True)
