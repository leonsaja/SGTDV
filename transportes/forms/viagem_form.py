from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms

from ..models import PassageiroViagem, Viagem


class ViagemForm(forms.ModelForm):
    class Meta:
        model=Viagem
        fields='__all__'
        widgets = {
            'motorista':s2forms.Select2Widget(),
                
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_saida'].widget.attrs.update({'class':'mask-hora'})
        self.fields['data_viagem'].widget.attrs.update({'class':'mask-data'})

    

class PassageiroViagemForm(forms.ModelForm):

    class Meta:
        model=PassageiroViagem
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['acompanhante'].widget.attrs.update({'class':'form-control'})
        self.fields['local_exame'].widget.attrs.update({'class':'form-control'})
        self.fields['local_espera'].widget.attrs.update({'class':'form-control'})
        self.fields['telefone'].widget.attrs.update({'class':'mask-telefone form-control'})

PassageiroViagemSet=inlineformset_factory(Viagem,PassageiroViagem,form=PassageiroViagemForm, extra=1)



