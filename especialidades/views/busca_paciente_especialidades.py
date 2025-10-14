from django.views.generic import ListView
from django.urls import reverse_lazy
from especialidades.models import PacienteEspecialidade
from rolepermissions.decorators import has_role_decorator
import re
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','regulacao','secretario','coordenador','acs'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class PacienteEspecialidadeSearchView(ListView):
   
    model = PacienteEspecialidade
    template_name = 'buscar_paciente_especialidade.html'
    paginate_by = 10
    pk_url_kwarg = 'id'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar', None)
        qs = PacienteEspecialidade.objects.select_related('paciente', 'especialidade', 'procedimento').all()

        if buscar:
            cpf_cns_limpo = re.sub(r'\D', '', buscar)
            
            if len(cpf_cns_limpo) == 11:
                qs = qs.filter(paciente__cpf=cpf_cns_limpo)
            elif len(cpf_cns_limpo) == 15:
                qs = qs.filter(paciente__cns=cpf_cns_limpo)
            else:
                qs = qs.filter(paciente__nome_completo__unaccent__icontains=buscar)
            
        return qs