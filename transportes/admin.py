from django.contrib import admin

from transportes.models import Carro, PassageiroViagem, Viagem

admin.site.register(Viagem)

admin.site.register(PassageiroViagem)

admin.site.register(Carro)
