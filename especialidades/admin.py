from django.contrib import admin

from .models import Especialidade, PacienteEspecialidade,AtendimentoEspecialidade

admin.site.register(AtendimentoEspecialidade)
admin.site.register(Especialidade)
admin.site.register(PacienteEspecialidade)