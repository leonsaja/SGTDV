from django.db import models
from cidadao.models import Cidadao
from profissionais.models import Profissional


class TipoEspecialidade(models.Model):
    nome=models.CharField(max_length=255, verbose_name='Especialidade')

class Especialidade (models.Model):

    TIPO_CLASSIFICACAO=(
        ('1','NORMAL'),
        ('2','URGÊNCIA'),
    )
    TIPO_CONSULTA=(
        ('1','CONSULTA'),
        ('2','RETORNO'),
    )
    paciente=models.ForeignKey(Cidadao,verbose_name='Paciente', on_delete=models.SET_NULL, null=True)
    especialidade=models.ForeignKey(TipoEspecialidade, on_delete=models.SET_NULL,null=True)
    data_pedido=models.DateField(verbose_name='Data do Pedido')
    profissional=models.ForeignKey(Profissional,verbose_name='Profissional',on_delete=models.SET_NULL, null=True)
    classficacao=models.CharField(max_length=1, verbose_name='Classificação',help_text='TIPO DE URGENCIA')
    tipo_consulta=models.CharField(max_length=1, verbose_name='Tipo de Consulta', )
    observacao=models.TextField(verbose_name='Observação',null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)