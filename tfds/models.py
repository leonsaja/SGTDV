from django.db import models
from cidadao.models import Cidadao
from localflavor.br.models import BRCPFField


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

   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='paciente')
   municipio_origem=models.CharField(verbose_name='Municipio Origem', max_length=120,null=False,blank=False,default='Santo Antônio do Jacinto-MG')
   municipio_destino=models.CharField(verbose_name='Municipio Destino', max_length=120,null=False,blank=False)
   data=models.DateField(verbose_name='Data')
   grs=models.CharField(verbose_name='GRS',max_length=50,null=False,blank=False,default='Pedra Azul-MG')
   especialidade=models.CharField(verbose_name='Especialidade', max_length=100, null=False, blank=False)

   #Dados para Acompanhante
   tem_acompanhante=models.CharField(verbose_name='Tem Acompanhante',null=False,blank=False,max_length=1,choices=ACOMPANHANTE)
   acompanhante=models.CharField(verbose_name='Acompanhante',null=True,blank=True, max_length=200)
   rg=models.CharField(max_length=10,verbose_name='RG', null=True,blank=True)
   cpf=BRCPFField(verbose_name='CPF', max_length=11, null=True,blank=True)
   cns=models.PositiveBigIntegerField(verbose_name='CNS',null=True,blank=True, help_text='Digite o cartão do SUS com 15 digitos')

   status=models.CharField(verbose_name='Avaliar Recibo Pag. de TFD',max_length=1,choices=STATUS,default='1')
   criado_por=models.CharField(verbose_name='Criado por ', max_length=200,null=True,blank=True)
   aprovado_por=models.CharField(verbose_name='Aprovado por ',max_length=200,null=True,blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.paciente.nome_completo}'
   
   def total_pag(self):
      items=ProcedimentoSia.objects.prefetch_related('recibo_tfd','codigosia').filter(recibo_tfd=self)

      total=0
      for item in items:
      
            total+=item.codigosia.subtotal*item.qtd_procedimento
           
      return total
  
class ProcedimentoSia(models.Model):
   
   qtd_procedimento=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
   recibo_tfd=models.ForeignKey(ReciboTFD,on_delete=models.CASCADE,related_name='procedimento_recibo_tfd')
   codigosia=models.ForeignKey("CodigoSIA",on_delete=models.PROTECT,related_name='procedimento_codigo')



   def soma(self):
      total=0
      total=self.codigosia.subtotal * self.qtd_procedimento
      return total

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   
class CodigoSIA(models.Model):

   codigo=models.CharField(max_length=10, verbose_name='Código',null=False,blank=False,unique=True)
   nome_proced=models.TextField(verbose_name='Nome do Procedimento',null=False,blank=False)
   valor_unitario=models.DecimalField(verbose_name='Valor Unitário', null=False,blank=False,max_digits=5,decimal_places=2)
   valor_contrapartida=models.DecimalField(verbose_name='Contra Partida', null=True,blank=True,max_digits=5,decimal_places=2)
   subtotal=models.DecimalField(verbose_name='Total',null=True,blank=True,max_digits=5,decimal_places=2 )
   
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
   
   """ def total(self):
      items=ProcedimentoSia.objects.filter(codigosia=self)
      total=0
            
      for item in items:
             
             print('destino', item.recibo_tfd.municipio_destino)
             total=0
             print('dados',self.subtotal,item.qtd_procedimento)
             total=self.subtotal * item.qtd_procedimento
             print('total',total)
      return total"""
   
   def valor_total_sigtap(self):
      items=ProcedimentoSia.objects.filter(codigosia=self)
      total=0
      
      for item in items:
         if self.codigo=='0803010125':
            if item.qtd_procedimento==1:
               total+=self.valor_unitario*16
            elif item.qtd_procedimento>1: 
               total+=(item.qtd_procedimento*16)*item.codigosia.valor_unitario

         elif self.codigo=='0803010109':
            if item.qtd_procedimento==1:
               total+=self.valor_unitario*16
            elif item.qtd_procedimento>1: 
                total+=(item.qtd_procedimento*16)*item.codigosia.valor_unitario

         else:
            total+=item.qtd_procedimento*self.valor_unitario
            
         return total  
      
   def valor_comp_mun(self):
       items=ProcedimentoSia.objects.filter(codigosia=self)
       vlr_comp=0
       total=0
       for item in items:
         vlr_comp=item.qtd_procedimento*self.subtotal
         total=vlr_comp-self.valor_total_sigtap()
         
       
       return total


      
     
   def __str__(self):
      return str(self.codigo)
   
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
   acompanhante=models.CharField(verbose_name='Acompanhante',null=True,blank=True, max_length=200)
   rg=models.CharField(max_length=10,verbose_name='RG', null=True,blank=True)
   cpf=BRCPFField(verbose_name='CPF', max_length=11, null=True,blank=True)
   cns=models.PositiveBigIntegerField(verbose_name='CNS', null=True,blank=True, help_text='Digite o cartão do SUS com 15 digitos')
       
   meio_transporte=models.CharField(max_length=1,null=False, blank=False,verbose_name='Meio de Transporte', choices=MEIO_TRANSPORTE)
   quant_passagem_paciente=models.PositiveIntegerField(verbose_name='Qta de Passagem',null=False, blank=False)
   quant_passagem_acompanhante=models.PositiveBigIntegerField(verbose_name='Qta  Passagem',null=True, blank=True)
   trecho =models.CharField(verbose_name='Trecho', null=False, blank=False, max_length=200 )
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
      if self.valor_acompanhante_sia and self.codigo_sia_acompanhante and self.acompanhante and self.quant_passagem_acompanhante:
         total=self.valor_paciente_sia+self.valor_acompanhante_sia
         return total
      return self.valor_paciente_sia
   
   def qta_passagem(self):
     
      resul=0
      if self.valor_acompanhante_sia and self.codigo_sia_acompanhante and self.acompanhante and self.quant_passagem_acompanhante:
         resul=self.quant_passagem_paciente+self.quant_passagem_acompanhante
         return resul
      
      else:
            return self.quant_passagem_paciente


