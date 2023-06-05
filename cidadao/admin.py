from django.contrib import admin

from cidadao.models import Cidadao, Endereco  # noqa

admin.site.register(Cidadao)
admin.site.register(Endereco)