from django.db import models

from cidadao.models import Cidadao


class ReciboTFD(models.Model):
   
   paciente=models.ForeignKey(Cidadao,on_delete=models.PROTECT,related_name='paciente')
   acompanhante=models.ForeignKey(Cidadao,null=True,blank=True, on_delete=models.PROTECT,related_name='recibo_acompanhante')
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
      return f'{self.paciente.nome_completo}'
   
   def total_pag(self):
      items=CodigoSIA.objects.filter(recibo_tfd=self)
      total=0

      for item in items:
         total+=item.valor_total

      return total
   
class CodigoSIA(models.Model):

   codigo=models.CharField(max_length=10, verbose_name='Código SIA',null=False,blank=False)
   valor_unitario=models.DecimalField(verbose_name='Valor Unitário', null=False,blank=False,max_digits=6,decimal_places=2)
   qtd_procedimento=models.PositiveBigIntegerField(verbose_name='Quantidade',null=False,blank=False)
   valor_total=models.DecimalField(verbose_name='Total',null=False,blank=False,max_digits=8,decimal_places=2 )
   recibo_tfd=models.ForeignKey(ReciboTFD,on_delete=models.CASCADE,related_name='recibo_codigo')

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

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
   qta_passagem=models.PositiveIntegerField(verbose_name='Quantidade de Passagem',null=False, blank=False, )
   trecho =models.CharField(verbose_name='Trecho', null=False, blank=False, max_length=200 )
   codigo_sia_paciente=models.CharField(verbose_name='Código SIA Paciente',max_length=10, null=True, blank=False)
   codigo_sia_acompanhante=models.CharField(verbose_name='Código SIA', max_length=10, null=True, blank=True)

   valor_paciente_sia=models.CharField(verbose_name='Valor', null=True,blank=False,max_length=30)
   valor_acompanhante_sia=models.CharField(verbose_name='Valor', null=True,blank=False,max_length=30)

   data_recibo=models.DateField(verbose_name='Data',null=True,blank=False)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.paciente.nome_completo}'