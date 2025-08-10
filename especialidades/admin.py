from django.contrib import admin

from .models import Especialidade, PacienteEspecialidade,AtendimentoEspecialidade, PacienteSia,ProcedimentosEspecialidade


@admin.register(PacienteEspecialidade)
class PacienteEspecialidadeAdmin(admin.ModelAdmin):
    search_fields=('paciente__nome_completo','paciente__cpf')


admin.site.register(Especialidade)
admin.site.register(AtendimentoEspecialidade)
admin.site.register(PacienteSia)
admin.site.register(ProcedimentosEspecialidade)