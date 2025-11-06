
from django import forms
from django.forms import ValidationError, inlineformset_factory
from especialidades.models import AtendimentoEspecialidade, PacienteEspecialidade
from django.utils import timezone
from datetime import date,timedelta
from datetime import date, timedelta
from dal import autocomplete

class AtendimentoEspecialidadeForm(forms.ModelForm):

    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    observacao=forms.CharField(label='Observação', required=False, widget=forms.Textarea( attrs={'rows':3,'cols':10}))

   
   
    class Meta:
        
        model=AtendimentoEspecialidade
        exclude=('criado_por','alterado_por',)
        widgets = {
            
            'especialidade':autocomplete.ModelSelect2(url='especialidades:especialidade-autocomplete'),
        }

    def clean(self):
        
        cleaned_data = super().clean()
        data=cleaned_data.get('data')
        especialidade=cleaned_data.get('especialidade')
        hoje=date.today()
        """ limite_minimo=hoje-timedelta(days=30)
        limite_maximo=hoje+timedelta(days=30)
        
        if data:
                if  data < limite_minimo:
                    if not self.instance.pk:
                        self.add_error(
                            f"data","A data do atendimento deve estar entre 30 dias antes e 30 dias depois da data atual."
                        )"""
        
        qs=AtendimentoEspecialidade.objects.filter(especialidade=especialidade,data=data).exists()

        if not self.instance.pk:
            if qs:
                self.add_error(
                            f"data","Existe um atendimento com essa data, o sistema só permitir um atendimento ao dia.")

        
        
        formset_prefix = 'paciente' 
        total_pacientes = 0
        
        pacientes_ids_cadastrados = set()
        
        try:
            total_forms_key = f'{formset_prefix}-TOTAL_FORMS'
            num_forms = int(self.data[total_forms_key])
        except (KeyError, ValueError):
            num_forms = 0

        for i in range(num_forms):
            paciente_key = f'{formset_prefix}-{i}-paciente'
            
            # O valor que vem do formulário é o ID do PacienteEspecialidade
            paciente_especialidade_id = self.data.get(paciente_key)
            delete = self.data.get(f'{formset_prefix}-{i}-DELETE')

            if delete == 'on':
                continue

            if paciente_especialidade_id and paciente_especialidade_id.strip():
                
                # A validação técnica é feita pelo ID
                if paciente_especialidade_id in pacientes_ids_cadastrados:
                    
                    # Se for duplicado, buscamos o nome para a mensagem
                    paciente_nome = 'Paciente (ID: {})'.format(paciente_especialidade_id)
                    
                    try:
                        # Busca o objeto PacienteEspecialidade pelo ID
                        paciente_obj = PacienteEspecialidade.objects.get(pk=paciente_especialidade_id)
                        # Acessa o objeto Cidadao (paciente) e pega o nome completo
                        paciente_nome = paciente_obj.paciente.nome_completo
                    except PacienteEspecialidade.DoesNotExist:
                        pass 
                        
                    # Adiciona um erro ao formulário principal usando o NOME para identificação
                    self.add_error(
                        'especialidade',
                        f"O paciente '{paciente_nome}' já está incluído neste atendimento. Remova a entrada duplicada."
                    )
                    
                else:
                    # Se for único, adiciona o ID ao conjunto e conta
                    pacientes_ids_cadastrados.add(paciente_especialidade_id)
                    total_pacientes += 1

                        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs.update({'class':'mask-hora'})
      
  
class GerarPDFAtendimentoForm(forms.Form):
    
    ORDEM=(
        
        ('1','Nome (A - Z)'),
        ('2','Nome (Z - A)'),
        ('3','Horário (00:00 - 23:59)'),
        ('5','Procedimento (A - Z)'),
        ('6','Procedimento (Z - A)'),
        ('7','Estabelecimento (A - Z)'),
        ('8','Estabelecimento (Z - A)'),

    )
    ordenar=forms.ChoiceField(label='Ordenar por ',required=True, widget=forms.Select,choices=ORDEM)


 

       