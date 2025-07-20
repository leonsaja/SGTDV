from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms

from ..models import PassageiroViagem, Viagem
from profissionais.models import Profissional
from transportes.models import Carro
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
            'carro':s2forms.Select2Widget(),
                
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_saida'].widget.attrs.update({'class':'mask-hora'})
        motoristas = Profissional.objects.select_related('estabelecimento').filter(cargo=7)
        carros=Carro.objects.filter(status=1)
       
        self.fields['motorista'].queryset = motoristas
        self.fields['carro'].queryset = carros

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
        
PassageiroViagemSet=inlineformset_factory(Viagem,PassageiroViagem,form=PassageiroViagemForm, extra=1, min_num=1,validate_min=True)



