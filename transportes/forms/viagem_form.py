from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms
from dal import autocomplete
from django.core.exceptions import ValidationError

from ..models import PassageiroViagem, Viagem
from profissionais.models import Profissional
from transportes.models import Carro
from datetime import date, timedelta

class ViagemForm(forms.ModelForm):
    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
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
        exclude=('criado_por','alterado_por',)
        widgets = {
            'motorista':autocomplete.ModelSelect2(url='profissionais:profissional-autocomplete'),
            'carro':s2forms.Select2Widget(),
            'destino_viagem':autocomplete.ModelSelect2(url='transportes:destino-autocompleto'),

        }

    def clean(self):
        
        
        cleaned_data = super().clean()
        carro = cleaned_data.get('carro')
        status = cleaned_data.get('status')
        motorista = cleaned_data.get('motorista')
        data=cleaned_data.get('data_viagem')
        status = self.cleaned_data.get('status')
        obs=self.cleaned_data.get('observacao')
        
        hoje=date.today()
        limite_minimo=hoje-timedelta(days=30)
        limite_maximo=hoje+timedelta(days=15)
       

        if status=='3':
            if not obs:
                self.add_error('observacao', 'Este campo é obrigatório. Por favor, informar motivo do cancelamento da viagem ')
        
        if data:
            if  data < limite_minimo or data > limite_maximo:
                if not self.instance.pk:
                    self.add_error(
                        f"data_viagem","A data deve estar entre 30 dias antes e 30 dias depois da data atual."
                    )
            
        
        if status=='1':
             qs=Viagem.objects.select_related('carro','motorista','destino_viagem').filter(carro=carro,status=status)
             
             if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
             
             if qs.exists():
                self.add_error('carro','Existe uma viagem com esse carro com status aguardando, por favor, concluir viagem anterior.')
        
            
        
        if status == '2' and not motorista:
            self.add_error('motorista', "O campo 'motorista' é obrigatório para viagens concluídas.")
        
        if status =='2' and motorista:
            qs=Viagem.objects.select_related('carro','motorista','destino_viagem').filter(data_viagem=data,status=status,motorista=motorista)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('motorista','Foi registrada uma viagem com este motorista, com status "concluído" e na data informada. Por favor, confirme se o nome do motorista está correto.')


         
        formset_prefix = 'passageiro' # Use o prefixo que você definiu
        total_passageiros = 0
        
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



