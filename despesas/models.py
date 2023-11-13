
from django.db import models

from profissionais.models import Profissional


class Diaria(models.Model):
    TIPO_DIARIA=(
        ('','---------'),
        ('1','Integral'),
        ('2','Meia'),
    )
    STATUS_REEMBOLSO=(
       ('1','SIM'),
       ('2','NÃO'),
    )

    profissional=models.ForeignKey(Profissional,on_delete=models.PROTECT,null=False, blank=False, related_name='profissionais')
    descricao=models.TextField(verbose_name='Descrição',null=False,blank=False)
    data_diaria=models.DateField(verbose_name='Data',null=False,blank=False)
    reembolso=models.CharField('Reembolso', max_length=1, choices=STATUS_REEMBOLSO)
    viagem_orig=models.CharField(verbose_name='Origem da Viagem',max_length=180,default='SANTO ANTÔNIO DO JACINTO-MG')
    viagem_dest=models.CharField(verbose_name='Destino da Viagem',max_length=200)
    conta=models.PositiveBigIntegerField(verbose_name='Conta',null=False,blank=False)
    fonte=models.PositiveIntegerField(verbose_name='Fonte',null=False,blank=False)
    obs=models.TextField(verbose_name='Observação',null=True,blank=True)
    tipo_diaria=models.CharField(max_length=1, verbose_name='Tipo de Diária',choices=TIPO_DIARIA,null=False,blank=False,default='')
    qta_diaria=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
    valor=models.CharField(verbose_name='Valor', max_length=50, null=False,blank=False)
    total=models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def valor_total(self):
       total=0

       if self.total:
          total+=self.total
       return total
    
    
    def __str__(self):
        return f'{self.profissional}'
    
    def total_desp(self):
      items=Reembolso.objects.filter(diaria=self)
      total=0

      if items:
        for item in items:
              if item.valor_desp:
                total+=item.valor_desp
              
        return total
      return ''
    
    def total_movimento(self):
      items=Reembolso.objects.filter(diaria=self)
      total=0

      if items:
        for item in items:
           if item.valor_mov:
              total+=item.valor_mov
           
        return total
      
      return ''
           
    
  
class Reembolso(models.Model):

    TIPOS_DESPESAS=(
        ('1','1-Hotel/Pousada'),
        ('2','2-Refeições e Lanches'),
        ('3','3-Estacionamento'),
        ('4','4-Passagens'),
        ('5','5-Táxi'),
        ('6','6-Mototáxi'),
        ('7','7-Locação de Veículo'),
        ('8','8-Combustivel'),
        ('9','9-Outros')
    )
    MOVIMENTACAO_FINANCEIRO=(
        ('1','1-Valores Adiantados ao Beneficiário'),
        ('2','2-Total Geral das despesas Comprovadas'),
        ('3','3-Diferença Apurada: Maior'),
        ('4','4-Diferença Apurada: Menor'),
        ('5','5-Valor Reembolsado ao Colaborador' ),
        ('6','6-Valor Dev. pelo Colaborador à Empresa')

    )

    descricao=models.CharField(verbose_name='Descrição',choices=TIPOS_DESPESAS,null=True,blank=True, max_length=1)
    diaria=models.ForeignKey(Diaria,on_delete=models.PROTECT,related_name='reembolsos',null=False,blank=False)
    movimentacao=models.CharField(verbose_name='Movimentação', choices=MOVIMENTACAO_FINANCEIRO, null=True,blank=True, max_length=1)
    valor_mov=models.DecimalField(max_digits=8,decimal_places=2, verbose_name='Valor',null=True, blank=True,default='')
    valor_desp=models.DecimalField(max_digits=8,decimal_places=2,verbose_name= 'Valor',null=True,blank=True,default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'