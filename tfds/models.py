from decimal import Decimal
from django.db import models
from cidadao.models import Cidadao
from transportes.models import Carro

class ReciboTFD(models.Model):
   
   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='paciente')
   acompanhante=models.ForeignKey(Cidadao,null=True,blank=True, on_delete=models.PROTECT,related_name='recibo_acompanhante')
   municipio_origem=models.CharField(verbose_name='Municipio Origem', max_length=120,null=False,blank=False,default='Santo Antônio do Jacinto-MG')
   municipio_destino=models.CharField(verbose_name='Municipio Destino', max_length=120,null=False,blank=False)
   data=models.DateField(verbose_name='Data')
   grs=models.CharField(verbose_name='GRS',max_length=50,null=False,blank=False,default='Pedra Azul-MG')
   especialidade=models.CharField(verbose_name='Especialidade', max_length=100, null=False, blank=False)
   
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.paciente.nome_completo}'
   
   def total_pag(self):
      items=CodigoSIA.objects.filter(recibo_tfd=self)
      total=0

      for item in items:
         total+=item.valor_total
      return total
   
class ProcedimentoSia(models.Model):
   
   qtd_procedimento=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
   recibo_tfd=models.ForeignKey(ReciboTFD,on_delete=models.CASCADE,related_name='procedimento_recibo_tfd')
   codigosia=models.ForeignKey("CodigoSIA",on_delete=models.CASCADE,related_name='procedimento_codigo')


   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


class CodigoSIA(models.Model):

   codigo=models.CharField(max_length=10, verbose_name='Código',null=False,blank=False,unique=True)
   nome_proced=models.TextField(verbose_name='Nome do Procedimento',null=False,blank=False)
   valor_unitario=models.DecimalField(verbose_name='Valor Unitário', null=False,blank=False,max_digits=5,decimal_places=2)
   valor_contrapartida=models.DecimalField(verbose_name='Contra Partida', null=True,blank=True,max_digits=5,decimal_places=2)
   """    valor_total=models.DecimalField(verbose_name='Total',null=True,blank=False,max_digits=5,decimal_places=2 ) """
   
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)



   def soma(self):
      
      total=0
      
      if (self.valor_contrapartida):
         total+=self.valor_contrapartida+self.valor_unitario
         
         
         return total
      return self.valor_unitario
         

   def __str__(self):
      return str(self.codigo)
   
class  ReciboPassagemTFD(models.Model):

   MEIO_TRANSPORTE=(
      ('1','1-TERRESTRE'),
      ('2','2-AÉREO'),
      ('3','3-OUTROS')
   )

   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='recibo_passagem_paciente')
   acompanhante=models.ForeignKey(Cidadao,null=True,blank=True, on_delete=models.PROTECT,related_name='recibo_passagem_acompanhante')
   meio_transporte=models.CharField(max_length=1,null=False, blank=False,verbose_name='Meio de Transporte', choices=MEIO_TRANSPORTE)
   quant_passagem_paciente=models.PositiveIntegerField(verbose_name='Qta de Passagem',null=False, blank=False)
   quant_passagem_acompanhante=models.PositiveBigIntegerField(verbose_name='Qta  Passagem',null=True, blank=True)
   trecho =models.CharField(verbose_name='Trecho', null=False, blank=False, max_length=200 )
   codigo_sia_paciente=models.CharField(verbose_name='Código SIA', max_length=10,null=True, blank=False)
   codigo_sia_acompanhante=models.CharField(verbose_name='Código SIA', max_length=10, null=True, blank=True)
   valor_paciente_sia=models.DecimalField(verbose_name='Valor', max_digits=8,decimal_places=2,null=False,blank=False)
   valor_acompanhante_sia=models.DecimalField(verbose_name='Valor', max_digits=8,decimal_places=2, null=True,blank=True)
   data_recibo=models.DateField(verbose_name='Data',null=True,blank=False)
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
            return '-'


class RegistroTransporte(models.Model):


   STATUS_CHOICES=(
      ('1','SIM'),
      ('2','NÃO,PACIENTE UTILIZOU RECURSOS PROPRIO'),
      ('3','NÃO,PERDEU A CONSULTA'),
      ('4','NÃO, SEM INFORMAÇÃO')
   )
   TIPO_ATENDIMENTO=(
      ('1','EVENTUAL'),
      ('2','ROTINEIRO'),
   )

   ACOMPANHANTE=(
      ('1','SIM'),
      ('2','NÃO'),
   )

   ATEND_ZONA_RURAL=(
      ('1','SIM'),
      ('2','NÃO'),
   )
  
   paciente=models.ForeignKey(Cidadao,null=False,blank=False,verbose_name='Paciente',on_delete=models.PROTECT)
   status=models.CharField(verbose_name='Transporte Atendido',max_length=1, choices=STATUS_CHOICES)
   dt_atendimento=models.DateField(verbose_name='Data de Atendimento')
   placa=models.ForeignKey(Carro, null=False, blank=False, verbose_name='Carro',on_delete=models.PROTECT)
   tipo_atend=models.CharField(verbose_name='Tipo Atendimento',max_length=1, choices=TIPO_ATENDIMENTO, null=False, blank=False)
   acompanhante=models.CharField(verbose_name='Tem Acompanhante',null=False,blank=False,max_length=1,choices=ACOMPANHANTE)
   atend_zona_rural=models.CharField(verbose_name='Atend. Zona Rural',max_length=1,choices=ATEND_ZONA_RURAL)
   origem=models.CharField(verbose_name='Origem',null=False, blank=False, max_length=200, default='SANTO ANTÔNIO DO JACINTO-MG')
   dist_percorrida=models.PositiveBigIntegerField(verbose_name='Distância Percorrida', null=False, blank=False)
   Quant_proced_paciente=models.PositiveBigIntegerField(verbose_name='Quantidade Procedimento 08.03.01.012-5',null=False,blank=False)
   Quant_proced_acompanhante=models.PositiveBigIntegerField(verbose_name='Quantidade Procedimento 08.03.01.010-9',null=True,blank=True)