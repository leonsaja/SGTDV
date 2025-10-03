from django import forms
from django.forms import ValidationError, inlineformset_factory
from cidadao.models import Cidadao
from dal import autocomplete

from especialidades.models import AtendimentoEspecialidade,PacienteSia

class PacienteSiaForm(forms.ModelForm):
     
    
     
     class Meta:
        
        model=PacienteSia
        fields=('hora','paciente','status',)
        widgets = {
            'paciente': autocomplete.ModelSelect2(
                url='especialidades:paciente-autocomplete',
                attrs={
                    'data-placeholder': 'Digite para buscar paciente...',
                    'data-minimum-input-length': 1,
                },
               forward=['atendimento-especialidade']

            ),
        }
    
   
   
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class':'form-control'})
        self.fields['hora'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control'})
        self.parent_instance = kwargs.pop('parent_instance', None) 



     def clean(self):
        cleaned_data = super().clean()
        
        paciente = cleaned_data.get('paciente')
        
        # 1. Obter a instância do AtendimentoEspecialidade (o objeto pai)
        atendimento = None
        if self.instance.pk:
            atendimento = self.instance.atendimento_paciente
        elif self.parent_instance:
            atendimento = self.parent_instance
        
        # Se os dados obrigatórios não estão presentes, deixa o Django lidar com os erros
        if not atendimento or not paciente:
            return cleaned_data

        # 2. Obter o Limite
        limite = atendimento.especialidade.limite_pacientes
        
        if limite > 0:
            # 3. Contar quantos pacientes JÁ estão vinculados a este Atendimento
            pacientes_no_atendimento = PacienteSia.objects.filter(
                atendimento_paciente=atendimento
            )

            # 4. Excluir a instância atual se for uma EDIÇÃO
            if self.instance.pk:
                pacientes_no_atendimento = pacientes_no_atendimento.exclude(pk=self.instance.pk)

            total_pacientes_atuais = pacientes_no_atendimento.count()

            # 5. Checar se o limite será excedido (total atual + 1 novo)
            if (total_pacientes_atuais + 1) > limite:
                
                # MENSAGEM DE ERRO ALTAMENTE PERSONALIZADA
                mensagem_erro = (
                    f'Limite excedido! A especialidade **"{atendimento.especialidade.nome}"** '
                    f'permite no máximo **{limite}** pacientes. '
                    f'Já existem **{total_pacientes_atuais+1}** pacientes agendados. '
                    f'Não é possível adicionar mais.'
                )
                
                # Levanta ValidationError associado a um campo específico.
                # Como o PacienteSia está em um formset, o erro deve ser anexado
                # a um campo no formulário filho (e não ao formulário pai).
                
                # Opção A: Erro no campo 'paciente' (mais comum)
                self._errors['paciente'] = self.error_class([mensagem_erro])
                
                # Ou, se quiser lançar um erro global no formulário filho:
                # raise forms.ValidationError(mensagem_erro)
                
        return cleaned_data


AtendPacienteSet=inlineformset_factory(AtendimentoEspecialidade,PacienteSia,form=PacienteSiaForm,extra=20, min_num=1,validate_min=True)
