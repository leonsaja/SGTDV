from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms
from dal import autocomplete
from django.core.exceptions import ValidationError

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

    def clean(self):

        cleaned_data = super().clean()
        carro = cleaned_data.get('carro')
        status=cleaned_data.get('status')
        motorista=cleaned_data.get('motorista')
        
        if status=='1':
             qs=Viagem.objects.select_related('carro','motorista').filter(carro=carro,status=status)
             
             if qs.exists():
                self.add_error('carro','Existe uma viagem com esse carro com status aguardando, por favor, concluir viagem anterior.')
        
             if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

        
        """ if status=='2':
            if not moto_id:
                self.add_error('motorista','Por favor, preencher  nome do motorista para concluir a viagem.')"""
        
        
        formset_prefix = 'passageiro' # Use o prefixo que você definiu
        
        total_passageiros = 0
        
        # Pega a quantidade de formulários no formset
        try:
            total_forms_key = f'{formset_prefix}-TOTAL_FORMS'
            num_forms = int(self.data[total_forms_key])
        except (KeyError, ValueError):
            num_forms = 0

        for i in range(num_forms):
            paciente_key = f'{formset_prefix}-{i}-paciente'
            acompanhante_key = f'{formset_prefix}-{i}-acompanhante'

            paciente = self.data.get(paciente_key)
            acompanhante = self.data.get(acompanhante_key)
            delete = self.data.get(f'{formset_prefix}-{i}-DELETE')

            # Conta passageiros e acompanhantes, mas ignora formulários que serão excluídos
            if delete == 'on':
                continue

            # Conta passageiros e acompanhantes apenas se os campos não estiverem vazios
            if paciente and paciente.strip():
                total_passageiros += 1
            if acompanhante and acompanhante.strip():
                total_passageiros += 1

        if carro and total_passageiros > carro.qta_passageiro:
           self.add_error('carro',f"O número de passageiros ({total_passageiros}) excede a capacidade do carro ({carro.qta_passageiro}))."
            )
            

        return cleaned_data
    
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
        widgets = {
            'paciente': autocomplete.ModelSelect2(url='cidadao:cidadao-autocomplete'),
        
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['acompanhante'].widget.attrs.update({'class':'form-control'})
        self.fields['local_exame'].widget.attrs.update({'class':'form-control'})
        self.fields['local_espera'].widget.attrs.update({'class':'form-control'})
        
PassageiroViagemSet=inlineformset_factory(Viagem,PassageiroViagem,form=PassageiroViagemForm, extra=1, min_num=1,validate_min=True)



