from django.db import models

from cidadao.models import Cidadao


class ReciboTFD(models.Model):
   
   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='paciente')
   acompanhante=models.ForeignKey(Cidadao,null=True,blank=True, on_delete=models.PROTECT,related_name='acompanhante')
   municipio_origem=models.CharField(verbose_name='Municipio Origem', max_length=120,null=False,blank=False,default='Santo Antônio do Jacinto-MG')
   municipio_destino=models.CharField(verbose_name='Municipio Destino', max_length=120,null=False,blank=False)
   data_criada = models.DateField(auto_now_add=True, help_text="Data de Criação")
   data_editada = models.DateField(auto_now=True, help_text="Data de Edição")
   data=models.DateField(verbose_name='Data')
   grs=models.CharField(verbose_name='GRS',max_length=50,null=False,blank=False,default='Pedra Azul-MG')
   especialidade=models.CharField(verbose_name='Especialidade', max_length=100, null=False, blank=False)
   
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.paciente.nome_completo
   
   def total_pag(self):
      items=CodigoSIA.objects.filter(recibo_tfd=self)
      total=0

      for item in items:
         total+=item.valor_total

      return total
   
class CodigoSIA(models.Model):

   codigo=models.PositiveIntegerField(verbose_name='Código SIA',null=False,blank=False)
   valor_unitario=models.DecimalField(verbose_name='Valor Unitário', null=False,blank=False,max_digits=6,decimal_places=2)
   qtd_procedimento=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
   valor_total=models.DecimalField(verbose_name='Total',null=False,blank=False,max_digits=8,decimal_places=2 )
   recibo_tfd=models.ForeignKey(ReciboTFD,on_delete=models.CASCADE,related_name='recibo_codigo')

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return str(self.codigo)
   
  

