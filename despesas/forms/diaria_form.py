from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms
from despesas.models import Diaria

class DiariaForm(forms.ModelForm):

    descricao=forms.CharField(label='Descrição', widget=forms.Textarea( attrs={'placeholder':'Digite a descrição da viagem...','rows':3,'cols':10}))
    obs=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
    data_diaria = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    valor = forms.CharField(
        label='Valor',widget=forms.TextInput(attrs={'placeholder':"R$ 0,00"}))

    total = forms.CharField(
        label='Subtotal',widget=forms.TextInput(attrs={'placeholder':'R$ 0,00','class':'money'}))
    
    class Meta:
        model=Diaria
        fields='__all__'
        widgets = {
            'profissional':s2forms.Select2Widget(),
           
        }
    def clean_total(self):
        data = self.cleaned_data["total"]
        return Decimal(data.replace(',', '.'))
       
    
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
    

    def clean(self):
        profissional=self.cleaned_data['profissional']
        data=self.cleaned_data['data_diaria']

        if Diaria.objects.filter(profissional=profissional).filter(data_diaria=data).exists():
            self.add_error('data_diaria', 'Já existe uma diaria do profissional com essa data')

        return super().clean()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['valor'].widget.attrs.update({'class':'mask-money'})





    

