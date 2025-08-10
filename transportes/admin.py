from django.contrib import admin

from transportes.models import Carro, PassageiroViagem, Viagem,RegistroTransporte

admin.site.register(Viagem)

admin.site.register(PassageiroViagem)

admin.site.register(Carro)
admin.site.register(RegistroTransporte)
