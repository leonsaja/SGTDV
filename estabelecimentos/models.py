from django.db import models


class Estabelecimento(models.Model):
    nome=models.CharField(max_length=255, verbose_name='Nome do Estabelecimento',null=False,blank=False,unique=True)
    cnes=models.PositiveBigIntegerField(verbose_name='CNES',null=False,blank=False, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.nome}'
    

class MicroArea(models.Model):
    microarea=models.PositiveIntegerField(verbose_name='Microárea',unique=True)
    estabelecimento=models.ForeignKey(Estabelecimento, verbose_name=('Estabelecimento'), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.microarea)

