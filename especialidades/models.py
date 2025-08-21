from django.db import models

from cidadao.models import Cidadao
from profissionais.models import Profissional



class Especialidade(models.Model):
    
    nome=models.CharField(max_length=255, verbose_name='Nome', unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
       return f'{self.nome}'
    
    def qta_pessoas_especialidade(self):
        pacientes=self.paciente_especialidades.filter().count()
        return pacientes
    
    def qta_pessoas_eletivo_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='1').exclude(status='2').count()
        return pacientes
    
    def qta_pessoas_concluido_especialidade(self):
        pacientes=self.paciente_especialidades.filter(status='2').count()
        return pacientes
    
    def qta_pessoas_prioridade_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='2').exclude(status='2').count()
        return pacientes
    def qta_pessoas_urgencia_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='3').exclude(status='2').count()
        return pacientes
    
    class Meta:
        ordering = ["nome"]

class PacienteEspecialidade(models.Model):

    TIPO_CLASSIFICACAO=(
        ('1','ELETIVO'),
        ('2','PRIORIDADE'),
        ('3','URGÊNCIA'),
    )

    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
        ('3','CANCELADO'),
        ('4','AUSENTE'),
        ('5','EM TRATAMENTO'),
        ('6','ALTA'),

    )
    
    paciente=models.ForeignKey(Cidadao,verbose_name='Paciente',related_name='cidadao_especialidade', on_delete=models.PROTECT)
    especialidade=models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name='paciente_especialidades')
    data_pedido=models.DateField(verbose_name='Data do Pedido')
    classificacao=models.CharField(max_length=1, verbose_name='Classificação',choices=TIPO_CLASSIFICACAO, help_text='TIPO DE URGENCIA')
    procedimento=models.ForeignKey('ProcedimentosEspecialidade',verbose_name='Procedimento',on_delete=models.PROTECT,null=True)
    observacao=models.TextField(verbose_name='Observação',null=True, blank=True)
    status=models.CharField(verbose_name='Status', choices=STATUS, max_length=1,default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.paciente.nome_completo}'
    
    class Meta:
        ordering = ["-paciente__nome_completo"]
   
class AtendimentoEspecialidade(models.Model):
    ATEND_VIA=(
            ('1','CIMBAJE'),
            ('2','CEAE'),
            ('3','RECURSO PRÓPRIO'),
            ('4','PPI'),

        )
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','CONCLUÍDO'),
        ('3','CANCELADO'),
        

    )

    especialidade=models.ForeignKey(Especialidade,verbose_name='Especialidade',on_delete=models.PROTECT)
    data=models.DateField(verbose_name='Data do Atendimento',null=True,blank=False)
    atendimento_via=models.CharField(max_length=1, choices=ATEND_VIA,  verbose_name=' Atendimento Via',null=False, blank=False)
    local_atendimento=models.CharField(max_length=255,verbose_name='Local do Atendimento',null=False, blank=False)
    observacao=models.TextField(verbose_name='Observação',null=True,blank=True)
    hora=models.TimeField(verbose_name='Horário do Atendimento',null=True,blank=False)
    status=models.CharField(verbose_name='Status', choices=STATUS, max_length=1,default=1,null=True)


    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return f'{self.especialidade}'
    
    def qta_paciente_especialidade(self):
        total=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(paciente__status='2').count()
        return total
 
class ProcedimentosEspecialidade(models.Model):
    nome_procedimento=models.CharField(max_length=255,verbose_name='Procedimento',null=True,blank=False)

    def __str__(self):
        return f'{self.nome_procedimento}'
      
    class Meta:
        ordering = ["-nome_procedimento"]
  
class PacienteSia(models.Model):
    paciente=models.ForeignKey(PacienteEspecialidade,verbose_name='Paciente',on_delete=models.PROTECT)
    atendimento_paciente=models.ForeignKey(AtendimentoEspecialidade,on_delete=models.CASCADE,related_name='atend_paciente_especialidade')
    hora=models.TimeField(verbose_name='Horário',null=True,blank=True)

    class Meta:
        # AQUI ESTÁ A VALIDAÇÃO:
        # Garante que a combinação de atendimento_paciente e paciente seja única.
        unique_together = ('atendimento_paciente', 'paciente',)
        
        ordering = ["-paciente"]
        
    def __str__(self):
        return f'{self.paciente}'
    

    






