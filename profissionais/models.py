
from django.db import models
from localflavor.br.models import BRCPFField

from estabelecimentos.models import Estabelecimento, MicroArea


class Profissional(models.Model):
    
    SEXO=(
        ('','-----------'),
        ('F','FEMININO'),
        ('M','MASCULINO')
    )
    STATUS=(
        ('1','ATIVO'),
        ('2','DESATIVADO'),
    )
    TIPO_CARGO = (
        ('','-----------'),
        ('1','ACS'),
        ('2','COORDENADOR(A)'),
        ('3','DIGITADOR'),
        ('4','ENFERMEIRO'),
        ('5','FAXINEIRO'),
        ('6','MÉDICO'),
        ('7','MOTORISTA'),
        ('8','RECEPCIONISTA'),
        ('9','TEC.ENFERMAGEM'),
        ('10','Outros'),
    
    )
    nome_completo = models.CharField(verbose_name='Nome Completo',max_length=120, null=False, blank=False)
    email=models.EmailField(verbose_name='E-mail', unique=True,null=True,blank=True)
    cpf=BRCPFField(verbose_name='CPF',unique=True, max_length=11, null=False,blank=False)
    status=models.CharField(max_length=2, verbose_name='Status',choices=STATUS, default='1',null=False,blank=False )
    cns=models.PositiveBigIntegerField(verbose_name='CNS',unique=True, null=False,blank=False, help_text='Digite o cartão do SUS com 15 digitos.')
    cargo=models.CharField(verbose_name='Cargo:',null=False,blank=False,choices=TIPO_CARGO, max_length=2,default='')
    sexo=models.CharField(verbose_name='Sexo',max_length=1,choices=SEXO, null=False, blank=False,default='')
    dt_nascimento=models.DateField(verbose_name='Data de Nascimento', null=False,blank=False)
    telefone=models.CharField(verbose_name='Telefone', max_length=15,null=False,blank=False)
    endereco=models.ForeignKey("Endereco",on_delete=models.CASCADE)
    estabelecimento=models.ForeignKey(Estabelecimento, verbose_name=('Estabelecimento'), on_delete=models.SET_NULL,null=True, related_name='profissional_estabelecimento')
    microarea=models.ForeignKey(MicroArea,on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Micro área',help_text='Campo somente para ACS',related_name='profissional_microarea')
   
    def __str__(self):
        return f'{self.nome_completo}, CPF: {self.cpf}'
    
    def formt_cpf(self):
        cpf=self.cpf
        if cpf:
            if len(cpf) == 11:
                return ('{}.{}.{}-{}'.format( cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
        return cpf
 
class Endereco(models.Model):
    
   logradouro = models.CharField(max_length=100, null=False, blank=False)
   numero = models.CharField(max_length=10, null=False, blank=False)
   bairro = models.CharField(max_length=70, null=False, blank=False)
   complemento = models.CharField(max_length=100, null=False, blank=False)
   cep = models.CharField(verbose_name='CEP',max_length=10, null=False, blank=False)
   cidade = models.CharField(max_length=100, null=False, blank=False)
   estado = models.CharField(max_length=2, null=False, blank=False)
   
    
   def __str__(self):
       return f'{self.logradouro}, Nº:{self.numero}, Bairro:{self.bairro}'   
