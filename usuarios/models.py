from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRCPFField
from .managers import UsuarioManager

class PerfilUsuario(models.Model):
      TIPO_PERFIL=(
        ('1','1-ACS'),
        ('2','2-Coordenador'),
        ('3','3-Digitador'),
        ('4','4-Recepção'),
        ('5','5-Secretario'),
        ('6','6-Regulação'),
       
      )
      perfil=models.CharField(verbose_name='Tipo de perfil',choices=TIPO_PERFIL,unique=True, max_length=1, null=True,blank=False)

      class Meta:
         ordering = ["perfil"]

      def __str__(self):
          return  self.get_perfil_display()

class Usuario(AbstractUser):
     
     username = None
     nome_completo=models.CharField(verbose_name='Nome Completo', max_length=200, null=True, blank=False)
     email = models.EmailField(verbose_name='E-mail', null=True, blank=False,unique=True)
     cpf=BRCPFField(verbose_name='CPF', unique=True, null=True, blank=False)
     dt_nascimento=models.DateField(verbose_name='Data de Nascimento', null=False, blank=False)
     perfil=models.ManyToManyField(PerfilUsuario)

     
     USERNAME_FIELD = "cpf"
     REQUIRED_FIELDS = ['nome_completo','tipo_usuario','dt_nascimento']

     objects = UsuarioManager()
     
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def formt_cpf(self):
        
        cpf=self.cpf
        if cpf:
            if len(cpf) == 11:
                return ('{}.{}.{}-{}'.format( cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
        
        return ' '

     def __str__(self):
        return f'{self.email}'
