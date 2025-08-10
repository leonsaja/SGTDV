from django.contrib import admin

from .models import CodigoSIA, ReciboPassagemTFD, ReciboTFD,ProcedimentoSia

admin.site.register(ReciboTFD)
admin.site.register(ReciboPassagemTFD)
admin.site.register(CodigoSIA)
admin.site.register(ProcedimentoSia)
