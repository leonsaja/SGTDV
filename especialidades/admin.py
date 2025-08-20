from django.contrib import admin

from .models import Especialidade, PacienteEspecialidade,AtendimentoEspecialidade, PacienteSia,ProcedimentosEspecialidade


@admin.register(PacienteEspecialidade)
class PacienteEspecialidadeAdmin(admin.ModelAdmin):
    search_fields=('paciente__nome_completo')

@admin.register(PacienteSia)
class PacienteSiaAdmin(admin.ModelAdmin):
    search_fields=('paciente__paciente__nome_completo',)
    
admin.site.register(Especialidade)
admin.site.register(AtendimentoEspecialidade)
admin.site.register(ProcedimentosEspecialidade)