from django import forms
from django.core.exceptions import ValidationError
from despesas.models import Diaria
from dal import autocomplete
from datetime import date,timedelta

class DiariaForm(forms.ModelForm):
    VALOR_FIXO_CHOICE=(
       ('1','SIM'),
       ('2','NÃO'),
    )
    STATUS_REEMBOLSO_CHOICE=(
       ('1','SIM'),
       ('2','NÃO'),
    )


    descricao=forms.CharField(label='Descrição da Viagem', widget=forms.Textarea( attrs={'placeholder':'Digite a descrição da viagem...','rows':3,'cols':10}))
    obs=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))
    valor_fixo=forms.ChoiceField(label='Valor é Fixo',required=True,widget=forms.RadioSelect,choices=VALOR_FIXO_CHOICE,initial='1',help_text='Valor da diária é fixa')
    data_diaria = forms.DateField(label='Data',widget=forms.DateInput( \
        format='%Y-%m-%d',attrs={ 'type': 'date',}),input_formats=('%Y-%m-%d',), )
    reembolso=forms.ChoiceField(label='Tem reembolso',required=True,widget=forms.RadioSelect,choices=STATUS_REEMBOLSO_CHOICE,initial='2',help_text='Existe reembolso na diária')
    class Meta:
        model=Diaria
        exclude=('status','criado_por','alterado_por','aprovado_por','total','descricao_rembolso','data_ult_nota_reembolso',)
        widgets = {
            'profissional':autocomplete.ModelSelect2(url='profissionais:profissional-autocomplete'),
            'viagem_dest':autocomplete.ModelSelect2(url='transportes:destino-autocompleto'),
        }

    def clean_qta_diaria(self):
        data = self.cleaned_data["qta_diaria"]
        if data==0:
            raise ValidationError('Digite um numero acima de 0.')
        
        return data
    
    def clean_conta(self):
        data_conta=str(self.cleaned_data.get('conta'))
        
        if data_conta:
            if len(data_conta)<=8:
                return data_conta   
            raise ValidationError('Digite a conta corretamente com até 8 digitos.')
        return data_conta
     
    def clean(self):
        cleaned_data = super().clean()
        profissional=cleaned_data.get('profissional')
        data=cleaned_data.get('data_diaria')
        descricao=cleaned_data.get('descricao')
        destino_viagem=cleaned_data.get('viagem_dest')
        valor_fixo=cleaned_data.get('valor_fixo')
        valor=cleaned_data.get('valor')
        
        hoje=date.today()
        limite_minimo=hoje-timedelta(days=30)
        limite_maximo=hoje+timedelta(days=7)

        
        valor_formatado = f"{destino_viagem.valor_localidade:.2f}".replace('.', ',')
        if valor_fixo=='1':
            if valor != destino_viagem.valor_localidade:
                self.add_error('valor', f'O valor informado não coincide com o valor padrão do destino da viagem que é (R$ {valor_formatado}).')
         
        if destino_viagem and descricao:
            destino=destino_viagem.nome 
            if destino.upper() not in descricao.upper():
                self.add_error('viagem_dest', 'Destino da viagem se encontra diferente da "DESCRIÇÃO DA VIAGEM" ou espaçamento entre as palavras ')
                

        insert = self.instance.pk == None

        data_diaria=self.instance.data_diaria
        diaria=Diaria.objects.select_related('profissional').filter(profissional=profissional).filter(data_diaria=data)
        
        if self.instance.pk:
            profissional_diaria=self.instance.profissional

            if data_diaria != data or profissional_diaria != profissional:
                 if diaria.exists():
                     self.add_error('data_diaria', 'Profissional já tem uma diaria com essa data.')

        elif insert:  #criação de diaria, verificar se já existe uma diaria com mesmo profissional e data.
             if diaria.exists():
                self.add_error('data_diaria', 'Profissional já tem uma diaria com essa data.')

        if data:
                if  data < limite_minimo or data > limite_maximo:
                    if not self.instance.pk:
                        self.add_error(
                            f"data_diaria","A data da diária deve estar entre 30 dias antes ou 7 dias depois da data atual."
                        )
# Form para aprovar ou reprovar diaria
class DiariaStatusForm(forms.ModelForm):
    
    class Meta:
        model=Diaria
        fields=['status']
        

