from django.db import models
from localflavor.br.models import BRCPFField
from estabelecimentos.models import MicroArea

class Cidadao(models.Model):
    
    SEXO=(
        ('F','Feminino'),
        ('M','Masculino'),
    )
    RACA=(
        ('1','AMARELA'),
        ('2','BRANCA'),
        ('3','PARDA'),
        ('4','PRETA'),
        ('5','OUTROS'),
       
    )
   
    nome_completo = models.CharField(verbose_name='Nome Completo',max_length=150, null=False, blank=False)
    email=models.EmailField(verbose_name='E-mail', unique=True,null=True,blank=True)
    rg=models.CharField(max_length=100,verbose_name='RG', null=True,blank=True)
    cpf=BRCPFField(verbose_name='CPF',unique=True, max_length=11, null=True,blank=True)
    cns=models.PositiveBigIntegerField(verbose_name='CNS', unique=True, null=False,blank=False, help_text='Digite o cartão do SUS com 15 digitos')
    sexo=models.CharField(verbose_name='Sexo:',max_length=1,choices=SEXO, null=False, blank=False)
    dt_nascimento=models.DateField(verbose_name='Data de Nascimento', null=False,blank=False)
    nome_mae=models.CharField(verbose_name='Nome da Mãe', max_length=150, null=True,blank=False)
    nome_pai=models.CharField(verbose_name='Nome do  Pai', max_length=150, null=True,blank=True)
    telefone=models.CharField(verbose_name='Telefone', max_length=15, null=True,blank=True)
    telefone1=models.CharField(verbose_name='Celular ', max_length=15,null=False,blank=False)
    
    microarea=models.ForeignKey(MicroArea,null=True,blank=False,on_delete=models.PROTECT, related_name='microarea_cidadao',verbose_name='MICRO ÁREA')
    raca=models.CharField(verbose_name='RAÇA/COR',max_length=1, choices=RACA, null=True, blank=False)
    nacionalidade=models.CharField(verbose_name='Município de nascimento',max_length=120, null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.cpf:
             return f'{self.nome_completo}, CPF:   {self.cpf}'  
        
        return f'{self.nome_completo}  CNS:   {self.cns}' 
       
    def formt_cpf(self):
        
        cpf=self.cpf
        if cpf:
            if len(cpf) == 11:
                return ('{}.{}.{}-{}'.format( cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
        
        return '-'
    

    def acompanhante(self):    
        return self.nome_completo.split()[0]

        
    class Meta:
        ordering = ["nome_completo"]
    
class Endereco(models.Model):

   ZONA=(
        ('1','---'),
        ('2','Urbana'),
        ('3','Rural'),
    )
   COD_LOGRADOURO=(
       ('1','---'),
       ('2','RUA'),
       ('3','FAZENDA'),
       ('4','PRACA'),
       ('5','TRAVESSA'),

   )
   cidadao=models.ForeignKey("Cidadao",on_delete=models.CASCADE, related_name='endereco_cidadao', null=True, blank=False)
   cod_logradouro=models.CharField(verbose_name="CÓD. LOGRADOURO", max_length=1,null=True,blank=False,choices=COD_LOGRADOURO,default='')
   logradouro = models.CharField(max_length=60, null=False, blank=False)
   numero = models.CharField(verbose_name='Número',max_length=10, null=False, blank=False)
   bairro = models.CharField(max_length=30, null=False, blank=False)
   complemento = models.CharField(max_length=100, null=False, blank=False)
   cep = models.CharField(verbose_name='CEP', max_length=10, null=False, blank=False)
   cidade = models.CharField(max_length=30, null=False, blank=False)
   estado = models.CharField( verbose_name='UF',max_length=2, null=False, blank=False)
   localizacao=models.CharField(verbose_name='Localização',max_length=1,choices=ZONA,null=True, blank=False,default='')

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

    
   def __str__(self):
       return f'{self.id}, {self.get_cod_logradouro_display()}, {self.logradouro}, Nº:{self.numero}, Bairro:{self.bairro}'   


   class Meta:
        ordering = ["logradouro"]