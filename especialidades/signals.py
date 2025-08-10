from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AtendimentoEspecialidade, PacienteSia, PacienteEspecialidade


@receiver(post_save, sender=AtendimentoEspecialidade)
def update_pacientes_status(sender, instance, created, **kwargs):
    # Verificamos se o status do AtendimentoEspecialidade foi atualizado para '2' (Concluído)
    if instance.status == '2':
        # Encontra TODOS os objetos PacienteSia que estão linkados a este atendimento.
        # Usa .filter() para obter um QuerySet que pode conter múltiplos objetos.
        pacientes_sia = PacienteSia.objects.filter(atendimento_paciente=instance)

        # Se houver pacientes associados a este atendimento, itera sobre eles.
        if pacientes_sia.exists():
            for paciente_sia in pacientes_sia:
                # Pega o objeto PacienteEspecialidade associado.
                paciente_especialidade = paciente_sia.paciente

                # Atualiza o status do PacienteEspecialidade para '2' (Concluído).
                # Adicionamos uma verificação para evitar salvar se o status já estiver correto.
                if paciente_especialidade.status != '2':
                    paciente_especialidade.status = '2'
                    paciente_especialidade.save()
        else:
            # Lida com a situação onde não há PacienteSia para o atendimento.
            print(f"Nenhum PacienteSia encontrado para o AtendimentoEspecialidade ID: {instance.id}")