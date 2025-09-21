from rolepermissions.mixins import HasRoleMixin
from django.views.generic import ListView
from especialidades.models import PacienteEspecialidade
from transportes.models import PassageiroViagem
from django.db.models import Q
import re

class PacienteViagemSearchView(HasRoleMixin,ListView):
   
    model = PassageiroViagem
    template_name = 'viagem/buscar_paciente_viagem.html'
    paginate_by = 10
    pk_url_kwarg = 'id'
    allowed_roles=['recepcao','regulacao','secretario','coordenador','acs']

    def get_queryset(self):
        buscar = self.request.GET.get('buscar', None)
        qs = PassageiroViagem.objects.select_related('paciente','viagem').all().order_by('-viagem')

        if buscar:
            
            cpf_cns_limpo = re.sub(r'\D', '', buscar)
         
            if len(cpf_cns_limpo) == 11:
                qs = qs.filter(paciente__cpf=cpf_cns_limpo)
            elif len(cpf_cns_limpo) == 15:
                qs = qs.filter(paciente__cns=cpf_cns_limpo)
            else:
                qs = qs.filter(paciente__nome_completo__unaccent__icontains=buscar)
           
        return qs