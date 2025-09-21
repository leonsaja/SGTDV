
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
        ('1','ACS'),
        ('2','COORDENADOR(A)'),
        ('3','DIGITADOR'),
        ('4','ENFERMEIRO'),
        ('5','FAXINEIRO'),
        ('6','MÉDICO'),
        ('7','MOTORISTA'),
        ('8','RECEPCIONISTA'),
        ('9','SECRETARIO'),
        ('10','TEC.ENFERMAGEM'),
        ('11','DENTISTA'),
        ('12','Outros'),
    
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
    estabelecimento=models.ForeignKey("estabelecimentos.estabelecimento", verbose_name=('Estabelecimentos'), on_delete=models.SET_NULL,null=True, related_name='profissional_estabelecimento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.nome_completo}, CPF: {self.cpf}'
    
    def formt_cpf(self):
        cpf=self.cpf
        if cpf:
            if len(cpf) == 11:
                return ('{}.{}.{}-{}'.format( cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
        return cpf
    def profis(self):
        return self.nome_completo.split()[0]
    def acs(self):    
        return self.nome_completo.split()[0]

    class Meta:
        ordering = ["nome_completo"]