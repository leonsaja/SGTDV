from django.db import models

from cidadao.models import Cidadao
from profissionais.models import Profissional



class Especialidade(models.Model):
    
    nome=models.CharField(max_length=255, verbose_name='Nome da Especialidade', unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
       return self.nome
    
    def qta_pessoas_especialidade(self):
        pacientes=self.paciente_especialidades.count()
        return pacientes
    
    def qta_pessoas_aguardando_especialidade(self):
        pacientes=self.paciente_especialidades.filter(status='1').count()
        return pacientes
    
    def qta_pessoas_concluido_especialidade(self):
        pacientes=self.paciente_especialidades.filter(status='2').count()
        return pacientes
    
    def qta_pessoas_urgencia_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='2').count()
        return pacientes

class PacienteEspecialidade(models.Model):

    TIPO_CLASSIFICACAO=(
        ('1','NORMAL'),
        ('2','URGÊNCIA'),
    )
    TIPO_ATENDIMENTO=(
        ('1','CONSULTA'),
        ('2','RETORNO'),
        ('3','AVALIAÇÃO'),
    )
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
    )
    
    paciente=models.ForeignKey(Cidadao,verbose_name='Paciente', on_delete=models.PROTECT)
    especialidade=models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name='paciente_especialidades')
    data_pedido=models.DateField(verbose_name='Data do Pedido')
    profissional=models.ForeignKey(Profissional,verbose_name='ACS',on_delete=models.PROTECT, null=True,help_text='ACS')
    classificacao=models.CharField(max_length=1, verbose_name='Classificação',choices=TIPO_CLASSIFICACAO, help_text='TIPO DE URGENCIA')
    tipo_atendimento=models.CharField(max_length=1, choices=TIPO_ATENDIMENTO,  verbose_name='Tipo de Atendimento')
    observacao=models.TextField(verbose_name='Observação',null=True, blank=True)
    status=models.CharField(verbose_name='Status', choices=STATUS, max_length=1,default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.paciente.nome_completo}'
        
    
   

    



    