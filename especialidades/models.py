from django.db import models
from django.forms import ValidationError

from cidadao.models import Cidadao
from profissionais.models import Profissional
from django.db.models import Q



class Especialidade(models.Model):
    TIPO=(
        ('1','ESPECIALIDADE'),
        ('2','PROCEDIMENTO'),
    )
    nome=models.CharField(max_length=255, verbose_name='Nome', unique=True)
    tipo=models.CharField(max_length=1, verbose_name='Tipo',choices=TIPO,null=True,blank=False)
    limite_pacientes=models.IntegerField(verbose_name='Limite de Pacientes',null=True,blank=False,
        default=0, 
        help_text='Limite de pacientes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
       return f'{self.nome}'
    
    def qta_pessoas_especialidade(self):
        pacientes=self.paciente_especialidades.filter(Q(status='1')|Q(status='5')).count()
        return pacientes
    
    def qta_pessoas_eletivo_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='1').filter(Q(status='1')|Q(status='5')).count()
        return pacientes
    
    def qta_pessoas_concluido_especialidade(self):
        pacientes=self.paciente_especialidades.filter(Q(status='2')|Q(status='6')).count()
        return pacientes
    
    def qta_pessoas_prioridade_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='2').filter(Q(status='1')|Q(status='5')).count()
        return pacientes
    def qta_pessoas_urgencia_especialidade(self):
        pacientes=self.paciente_especialidades.filter(classificacao='3').filter(Q(status='1')|Q(status='5')).count()
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
        ('7','ACOMPANHAMENTO')

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

    criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)
    alterado_por=models.CharField(verbose_name='Alterado por ', max_length=200,null=True,blank=True)
    
    
    def __str__(self):
        return f'{self.paciente.nome_completo} - ({self.paciente.dt_nascimento.strftime("%d/%m/%Y")}) - ({self.procedimento.nome_procedimento}) - ({self.get_classificacao_display()})'
    
    class Meta:
        ordering = ["data_pedido"]
   
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
    
    criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)
    alterado_por=models.CharField(verbose_name='Alterado por ', max_length=200,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return f'{self.especialidade}'
    
    def qta_paciente_especialidade_concluido(self):
        atendimento_paciente_presente=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(status='2').count()
        total_concluido=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(paciente__status='2').count()
        if atendimento_paciente_presente>0:
            total=atendimento_paciente_presente
      
        elif total_concluido == 0:
              total=total_concluido
        else:
            total_ausente=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(status='1').count()
            total=total_concluido-total_ausente
        return total
    def qta_paciente_especialidade_ausente(self):
        total=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(status='1').count()
        if total:
            return total
        else:
            total=PacienteSia.objects.select_related('atendimento_paciente','procedimento').filter(atendimento_paciente=self).filter(paciente__status='4').count()
            return total
        
    class Meta:
        ordering = ["data"]
        
class ProcedimentosEspecialidade(models.Model):
    nome_procedimento=models.CharField(max_length=255,verbose_name='Procedimento',null=True,blank=False)

    def __str__(self):
        return f'{self.nome_procedimento}'
      
    class Meta:
        ordering = ["nome_procedimento"]
  
class PacienteSia(models.Model):
    STATUS=(
        ('1','AUSENTE'),
        ('2','CONCLUIDO'),


    )
    paciente=models.ForeignKey(PacienteEspecialidade,verbose_name='Paciente',related_name='paciente_sia_paciente_especialidade',on_delete=models.PROTECT)
    atendimento_paciente=models.ForeignKey(AtendimentoEspecialidade,on_delete=models.CASCADE,related_name='atend_paciente_especialidade')
    hora=models.TimeField(verbose_name='Horário',null=True,blank=True)
    status=models.CharField(verbose_name='Status', choices=STATUS, max_length=1,null=True,blank=True,help_text='Somente usa quando paciente faltou no atendimento')    
    class Meta:
        unique_together = ('atendimento_paciente', 'paciente',)
        ordering = ["paciente__paciente__nome_completo"]
        
    def __str__(self):
        return f'{self.paciente}'
    


    

    






