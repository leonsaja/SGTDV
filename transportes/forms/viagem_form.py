from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms

from ..models import PassageiroViagem, Viagem


class ViagemForm(forms.ModelForm):

    data_viagem = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
     
    class Meta:
        model=Viagem
        fields='__all__'
        widgets = {
            'motorista':s2forms.Select2Widget(),
                
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_saida'].widget.attrs.update({'class':'mask-hora'})

    

class PassageiroViagemForm(forms.ModelForm):

    class Meta:
        model=PassageiroViagem
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['acompanhante'].widget.attrs.update({'class':'form-control'})
        self.fields['local_exame'].widget.attrs.update({'class':'form-control'})
        self.fields['local_espera'].widget.attrs.update({'class':'form-control'})
        self.fields['telefone'].widget.attrs.update({'class':'form-control'})


"""    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        campo_relacionado = cleaned_data.get('viagem')
        acompanhante=cleaned_data.get('acompanhante')
        total=0
        for form in cleaned_data:
            print('TIPO',form)
"""
        

PassageiroViagemSet=inlineformset_factory(Viagem,PassageiroViagem,form=PassageiroViagemForm, extra=1, min_num=1,validate_min=True)



