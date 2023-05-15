from django.db import models


class Estabelecimento(models.Model):
    nome=models.CharField(max_length=255, verbose_name='Nome do Estabelecimento',null=False,blank=False,unique=True)
    cnes=models.PositiveBigIntegerField(verbose_name='CNES',null=False,blank=False, unique=True)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome
    

class MicroArea(models.Model):
    microarea=models.PositiveIntegerField(verbose_name='Microárea',unique=True)
    estabelecimento=models.ForeignKey(Estabelecimento, verbose_name=('Estabelecimento'), on_delete=models.CASCADE)

    
    def __str__(self):
        return str(self.microarea)

