
from decimal import Decimal
from django import forms
from django.forms import ValidationError, inlineformset_factory
from tfds.models import  ReciboTFD,ProcedimentoSia, CodigoSIA


class ProcedimentoSiaForm(forms.ModelForm):
    
    class Meta:
        
        model=ProcedimentoSia
        fields=('codigosia','qtd_procedimento')

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigosia'].widget.attrs.update({'class':'form-control'})
        self.fields['qtd_procedimento'].widget.attrs.update({'class':'form-control'})
        
    

class CodigoSiaForm(forms.ModelForm):
   
    nome_proced=forms.CharField(label='Nome do Procedimento', widget=forms.Textarea( attrs={'placeholder':'Descrição', 'rows':4,'cols':10}))
    valor_unitario = forms.CharField(label='VLR UNIT. T.SIGTAP ',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':"money"}))
    valor_contrapartida = forms.CharField(label='VLR COMP. MUNICIPAL ',required=False, widget=forms.TextInput(attrs={'placeholder':"R$ 0,00",'class':"money"}))

    class Meta:
        model=CodigoSIA
        exclude=('subtotal',)

    def clean_codigo(self):
        data = self.cleaned_data["codigo"]
        if data.isdigit():
             if len(data)==10:
                  return data
             raise ValidationError('Por favor, digite 10 digitos')
        raise ValidationError('Por favor, digite números')
    
    def clean_valor_unitario(self):
        data = self.cleaned_data["valor_unitario"]
        return Decimal(data.replace(',', '.'))
        
    def clean_valor_contrapartida(self):
        data = self.cleaned_data["valor_contrapartida"]
        if data:
            return Decimal(data.replace(',', '.'))
        data=Decimal('0.00')
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        codigo=cleaned_data.get('codigo')
        valor_passagem=cleaned_data.get('valor_passagem')
        
        if codigo == "0803010125" or codigo == '0803010109':
            if not valor_passagem:
                self.add_error('valor_passagem', 'Este campo é obrigatório.')

            
ProcedimentoSet=inlineformset_factory(ReciboTFD,ProcedimentoSia,form=ProcedimentoSiaForm,extra=1, min_num=1,validate_min=True)

