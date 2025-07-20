from django.contrib import admin

from cidadao.models import Cidadao, Endereco  # noqa

admin.site.register(Cidadao)

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    search_fields=('cidadao__nome_completo', 'logradouro')