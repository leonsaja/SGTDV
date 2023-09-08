from django.contrib import messages
from django.db import models

from cidadao.models import Cidadao
from profissionais.models import Profissional


class Viagem(models.Model):

   STATUS_VIAGEM=(
       ('1','AGUARDANDO'),
       ('2','CONCLUÍDO'),)
    

   data_viagem=models.DateField(verbose_name='Data da Viagem', null=False,blank=False)
   destino_viagem=models.CharField(verbose_name='Destino', max_length=180,null=False, blank=False)
   horario_saida=models.TimeField(verbose_name='Horario de Viagem')
   motorista=models.ForeignKey( Profissional, verbose_name='Motorista', on_delete=models.PROTECT)
   status=models.CharField(verbose_name='Status da Viagem',max_length=1, choices=STATUS_VIAGEM, null=False, blank=False, default=1)
   carro=models.ForeignKey('Carro',related_name='carro_viagens', on_delete=models.PROTECT)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)



   def __str__(self):
      return f'{self.destino_viagem}'


class PassageiroViagem(models.Model):
   
   paciente=models.CharField(verbose_name='Nome do Paciente', max_length=255,null=False, blank=False)
   acompanhante=models.CharField(null=True,blank=True, max_length=255, verbose_name='Acompanhante')
   local_exame=models.CharField(verbose_name='Local do Exame', max_length=150, null=True, blank=True)
   local_espera=models.CharField(verbose_name='Local de Espera', max_length=150,null=True, blank=True)
   viagem=models.ForeignKey("Viagem",on_delete=models.CASCADE, related_name='passageiros_viagens')
   telefone=models.CharField(verbose_name='telefone', blank=True, null=True, max_length=15, help_text='Sem caracteres especiais') 
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.paciente}'
   
class Carro(models.Model):
   nome=models.CharField(verbose_name='Nome do Carro', max_length=180, null=False, blank=False)
   placa=models.CharField(verbose_name='Placa do Carro', max_length=7,unique=True, help_text='Sem caracteres especiais(-)')
   foto=models.ImageField(verbose_name='Foto do carro', upload_to='media/carros', null=False, blank=False, default='')

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def __str__(self):
      return f'{self.nome}, Placa: {self.placa}'