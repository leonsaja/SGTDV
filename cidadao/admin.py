from django.contrib import admin

from cidadao.models import Cidadao, Endereco  # noqa


@admin.register(Cidadao)
class CidadaoAdmin(admin.ModelAdmin):
    search_fields=('nome_completo', 'cpf','dt_nascimento')
    
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    search_fields=('cidadao__nome_completo', 'logradouro')