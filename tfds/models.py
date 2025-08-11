import math
from django.db import models
from cidadao.models import Cidadao
from localflavor.br.models import BRCPFField
from decimal import Decimal
from especialidades.models import Especialidade

class ReciboTFD(models.Model):

   STATUS=(
        ('1','AGUARDANDO'),
        ('2','APROVADO'),
        ('3','REPROVADO'),
    )
   ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
   )

   PAGAMENTO_POR=(
      ('1','PIX'),
      ('2','CONTA'),
      
   )
   FORA_ESTADO=(
      ('1','SIM'),
      ('2','NÃO'),
   )
   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='paciente')
   municipio_origem=models.CharField(verbose_name='Município Origem', max_length=120,null=False,blank=False,default='Santo Antônio do Jacinto-MG')
   municipio_destino=models.CharField(verbose_name='Município Destino', max_length=120,null=False,blank=False)
   data=models.DateField(verbose_name='Data')
   grs=models.CharField(verbose_name='GRS',max_length=50,null=False,blank=False,default='Pedra Azul-MG')
   especialidade=models.ForeignKey(Especialidade,on_delete=models.PROTECT, verbose_name='Especialidade', null=False, blank=False)
   unid_assistencial=models.CharField(verbose_name='Unidade Assistencial',null=True, blank=False,max_length=240)
   
   #Dados para Acompanhante
   tem_acompanhante=models.CharField(verbose_name='Tem Acompanhante',null=False,blank=False,max_length=1,choices=ACOMPANHANTE)
   acompanhante=models.ForeignKey(Cidadao,verbose_name='Acompanhante',null=True,blank=True,on_delete=models.PROTECT)
   
   #Atendimento fora do estado
   atend_fora_estado=models.CharField(verbose_name='Atendimento fora do estado',null=True,blank=False,max_length=1,choices=FORA_ESTADO)
   qta_proced=models.PositiveBigIntegerField(verbose_name='Quant. Procedimento',null=True,blank=True)
   valor_passagem=models.DecimalField(verbose_name='Valor da Passagem', max_digits=8,decimal_places=2,null=True,blank=True)
   
   #formato de pagamento pix ou conta
   pagamento_por=models.CharField(verbose_name='PAGAMENTO POR',null=True,blank=False,max_length=1,choices=PAGAMENTO_POR)
   agencia=models.CharField(max_length=20, verbose_name='AGENCIA',null=True,blank=True)
   conta=models.CharField(max_length=200, verbose_name='CONTA',null=True,blank=True)
   pix=models.CharField(max_length=200, verbose_name='PIX',null=True,blank=True)

   status=models.CharField(verbose_name='Avaliar Recibo Pag. de TFD',max_length=1,choices=STATUS,default='1')
   criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)
   aprovado_por=models.CharField(verbose_name='Aprovado por ',max_length=200,null=True,blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   total_gasto=models.DecimalField(verbose_name='Total Gasto',max_digits=10,decimal_places=2,null=True,blank=True)

   def __str__(self):
      return f'{self.id} {self.paciente.nome_completo}'
   
   def calcular_total_gasto(self):
      items=ProcedimentoSia.objects.prefetch_related('recibo_tfd','codigosia').filter(recibo_tfd=self)

      total=0
      for item in items:
      
            total+=item.soma()
           
      return total

    # Sobrescreva o método save() para atualizar o campo total_gasto automaticamente
   def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
   def total_pag(self):
        return self.total_gasto
   
class ProcedimentoSia(models.Model):
   
   qtd_procedimento=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
   recibo_tfd=models.ForeignKey(ReciboTFD,on_delete=models.CASCADE,related_name='procedimento_recibo_tfd')
   codigosia=models.ForeignKey("CodigoSIA",on_delete=models.PROTECT,related_name='procedimento_codigo')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def valor_unid_sigtap(self):
      total=0
      if self.recibo_tfd.atend_fora_estado=='1':
         if self.codigosia.codigo=='0803010125':
            total=(self.codigosia.valor_unitario*self.recibo_tfd.qta_proced)
               
         elif self.codigosia.codigo=='0803010109':
            total=(self.codigosia.valor_unitario*self.recibo_tfd.qta_proced)
         else: 
            total=(self.codigosia.valor_unitario)
      
      elif self.recibo_tfd.atend_fora_estado=='2':
         if self.codigosia.codigo=='0803010125':
            total=(self.codigosia.valor_unitario*17)
               
         elif self.codigosia.codigo=='0803010109':
            total=(self.codigosia.valor_unitario*17)   
         else: 
            total=(self.codigosia.valor_unitario)
      return total
   
   def valor_total_sigtap(self):
      total=0
      total=self.qtd_procedimento*self.valor_unid_sigtap()
      
      return total
           
   def valor_comp_mun(self):
       total=0
       if self.recibo_tfd.atend_fora_estado=='1':
         total=self.soma()-self.valor_total_sigtap()
         
       elif self.recibo_tfd.atend_fora_estado=='2':
         if self.codigosia.codigo=='0803010125':
            total=self.soma()-self.valor_total_sigtap()
   
         elif self.codigosia.codigo=='0803010109':
              total=self.soma()-self.valor_total_sigtap()
         else:
            total=(self.codigosia.subtotal*self.qtd_procedimento)-self.valor_total_sigtap()
      
       return total
      
   def soma(self):
      total=0
      if self.recibo_tfd.atend_fora_estado=='1':
         if self.codigosia.codigo=='0803010125':
            total=self.qtd_procedimento*self.recibo_tfd.valor_passagem
         elif self.codigosia.codigo=='0803010109':
             total=self.qtd_procedimento*self.recibo_tfd.valor_passagem
         else:
            total=self.qtd_procedimento*self.codigosia.subtotal
            
      elif self.recibo_tfd.atend_fora_estado=='2':
         if self.codigosia.codigo=='0803010125':
                total=self.qtd_procedimento*self.codigosia.valor_passagem
            
         elif self.codigosia.codigo=='0803010109':
              total=self.qtd_procedimento*self.codigosia.valor_passagem
           
         else:
            total=self.codigosia.subtotal*self.qtd_procedimento
      return total
  
 
   def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Salva o recibo pai para atualizar o campo total_gasto
        self.recibo_tfd.save()       

        
class CodigoSIA(models.Model):

   codigo=models.CharField(max_length=10, verbose_name='Código',null=False,blank=False,unique=True)
   nome_proced=models.TextField(verbose_name='Nome do Procedimento',null=False,blank=False)
   valor_unitario=models.DecimalField(verbose_name='Valor Unitário', null=False,blank=False,max_digits=5,decimal_places=2)
   valor_contrapartida=models.DecimalField(verbose_name='Contra Partida', null=True,blank=True,max_digits=5,decimal_places=2)
   subtotal=models.DecimalField(verbose_name='Total',null=True,blank=True,max_digits=5,decimal_places=2 )
   valor_passagem=models.DecimalField(verbose_name='Valor da Passagem', null=True,blank=True,max_digits=5,decimal_places=2)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def save(self,*args, **kwargs):
      
      if not self.subtotal:
        if self.valor_contrapartida:
           self.subtotal=self.valor_unitario+self.valor_contrapartida
        else:
           self.subtotal=self.valor_unitario
           
      elif self.valor_contrapartida:
           self.subtotal=self.valor_unitario+self.valor_contrapartida
           
      else:
           self.subtotal=self.valor_unitario
           
      return super().save(*args, **kwargs)
   
     
   def __str__(self):
      return str("("+self.codigo +")" + " "+ self.nome_proced)
   
class ReciboPassagemTFD(models.Model):

   MEIO_TRANSPORTE=(
      ('1','1-TERRESTRE'),
      ('2','2-AÉREO'),
      ('3','3-OUTROS')
   )
   ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
   )

   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='recibo_passagem_paciente')
   #Dados para Acompanhante
   tem_acompanhante=models.CharField(verbose_name='Tem Acompanhante',null=False,blank=False,max_length=1,choices=ACOMPANHANTE)
   acompanhante=models.ForeignKey(Cidadao,verbose_name='Acompanhante',null=True,blank=True,on_delete=models.PROTECT)
   meio_transporte=models.CharField(max_length=1,null=False, blank=False,verbose_name='Meio de Transporte', choices=MEIO_TRANSPORTE)
   quant_passagem_paciente=models.PositiveIntegerField(verbose_name='Qta de Passagem',null=False, blank=False)
   quant_passagem_acompanhante=models.PositiveBigIntegerField(verbose_name='Qta  Passagem',null=True, blank=True)
   trecho =models.CharField(verbose_name='Trecho', null=False, blank=False, max_length=200,default='SANTO ANTÔNIO DO JACINTO-MG/BELO HORIZONTE-MG')
   codigo_sia_paciente=models.CharField(verbose_name='Código SIA', max_length=10,null=True, blank=False,default='0803010125')
   codigo_sia_acompanhante=models.CharField(verbose_name='Código SIA', max_length=10, null=True, blank=True)
   valor_paciente_sia=models.DecimalField(verbose_name='Valor', max_digits=8,decimal_places=2,null=False,blank=False)
   valor_acompanhante_sia=models.DecimalField(verbose_name='Valor', max_digits=8,decimal_places=2, null=True,blank=True)
   data_recibo=models.DateField(verbose_name='Data',null=True,blank=False)

   criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.paciente.nome_completo}'
   

   def valor_total_passagem(self):
      total=0
      if self.tem_acompanhante=='1':
         return self.valor_paciente_sia*self.quant_passagem_paciente
      return  self.valor_paciente_sia*self.quant_passagem_paciente
   
   def qta_passagem(self):
     
      resul=0
      if self.tem_acompanhante=='1':
         resul=self.quant_passagem_paciente+self.quant_passagem_acompanhante
         return resul
      
      else:
            return self.quant_passagem_paciente


   def total(self):
      total=0
      if self.tem_acompanhante=='1':
         return (self.quant_passagem_paciente*self.valor_paciente_sia)+(self.valor_acompanhante_sia*self.quant_passagem_acompanhante)
      return self.quant_passagem_paciente*self.valor_paciente_sia