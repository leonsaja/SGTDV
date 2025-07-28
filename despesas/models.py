
from django.db import models

from profissionais.models import Profissional
from decimal import Decimal

class Diaria(models.Model):
    TIPO_DIARIA=(
        ('','---------'),
        ('1','Integral'),
        ('2','Meia'),
        ('3','Integral+Meia'),
    )
    STATUS_REEMBOLSO=(
       ('1','SIM'),
       ('2','NÃO'),
    )

    STATUS=(
        ('1','AGUARDANDO'),
        ('2','APROVADO'),
        ('3','REPROVADO'),
    )
    profissional=models.ForeignKey(Profissional,on_delete=models.PROTECT,null=False, blank=False, related_name='profissionais')
    descricao=models.TextField(verbose_name='Descrição ',null=False,blank=False)
    data_diaria=models.DateField(verbose_name='Data',null=False,blank=False)
    reembolso=models.CharField('Reembolso', max_length=1, choices=STATUS_REEMBOLSO)
    viagem_orig=models.CharField(verbose_name='Origem da Viagem',max_length=180,default='SANTO ANTÔNIO DO JACINTO-MG')
    viagem_dest=models.CharField(verbose_name='Destino da Viagem',max_length=200)
    conta=models.PositiveBigIntegerField(verbose_name='Conta',null=False,blank=False,default=115223)
    fonte=models.PositiveIntegerField(verbose_name='Fonte',null=False,blank=False,default=15001002)
    obs=models.TextField(verbose_name='Observação',null=True,blank=True)
    tipo_diaria=models.CharField(max_length=1, verbose_name='Tipo de Diária',choices=TIPO_DIARIA,null=False,blank=False,default='')
    qta_diaria=models.DecimalField(verbose_name='Quantidade',null=False,blank=False,max_digits=2,decimal_places=1)
    valor=models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=10, null=False,blank=False)
    total=models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    status=models.CharField(verbose_name='Avaliar',max_length=1,choices=STATUS,default='1')
    criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)
    aprovado_por=models.CharField(verbose_name='Aprovado por ',max_length=200,null=True,blank=True)
    descricao_reembolso=models.TextField(verbose_name='Descrição Reembolso',null=True,blank=True)
    def valor_total(self):
       total=0

       if self.total:
          total+=self.total
       return total
    def form_conta(self):
       conta=str(self.conta)
       return ('{}-{}'.format(conta[:5],conta[5:]))
    
    def form_fonte(self):
       fonte=str(self.fonte)
       return ('{}-{}'.format(fonte[:4],fonte[4:]))
    
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
    
    def save(self,*args, **kwargs):
      meia=0
      diaria_meia=0

      if not self.total:
         if self.tipo_diaria =='1':
            self.total=self.qta_diaria*self.valor
         elif self.tipo_diaria=='2':
            meia=self.valor/2
            self.total=self.qta_diaria*meia
         else:
            diaria_meia=self.valor/2
            self.total=self.valor+diaria_meia
         
      else:
         if self.tipo_diaria =='1':
            self.total=self.qta_diaria*self.valor
            
         elif self.tipo_diaria=='2':
            meia=self.valor/2
            self.total=self.qta_diaria*meia

         else:
            diaria_meia=self.valor/2
            self.total=self.valor+diaria_meia
         
      return super().save(*args, **kwargs)

    def total_movimento(self):
      items=Reembolso.objects.filter(diaria=self)
      total=0

      if items:
        for item in items:
           if item.valor_mov:
              total+=item.valor_mov
           
        return total
      
      return ''

    def form_qta_diaria(self):
        meio=0
        valor=0
        if self.tipo_diaria =='1':
           valor=int(self.qta_diaria)
        elif self.tipo_diaria=='2':
            meio=self.qta_diaria/2
            valor=meio
        else:
           valor=self.qta_diaria
        return valor

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
    STATUS=(
        ('1','AGUARDANDO'),
        ('2','APROVADO'),
        ('3','REPROVADO'),
    )
    descricao=models.CharField(verbose_name='Descrição',choices=TIPOS_DESPESAS,null=True,blank=True, max_length=1)
    valor_desp=models.DecimalField(max_digits=8,decimal_places=2,verbose_name= 'Valor',null=True,blank=False)
    diaria=models.ForeignKey(Diaria,on_delete=models.PROTECT,related_name='reembolsos',null=False,blank=False)
    obs=models.CharField(verbose_name='OBSERVAÇÃO', null=True,blank=True, max_length=200)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_desp(self):
       total=0

       if self.valor_desp:
          total+=self.valor_desp

       return total

    def __str__(self):
        return f'{self.id}'
    
