from django.contrib import admin

from .models import Especialidade, PacienteEspecialidade,AtendimentoEspecialidade, PacienteSia

admin.site.register(Especialidade)
admin.site.register(PacienteEspecialidade)
admin.site.register(AtendimentoEspecialidade)
admin.site.register(PacienteSia)