from django.contrib import admin

from .models import Endereco, Profissional

admin.site.register(Profissional)

admin.site.register(Endereco)
