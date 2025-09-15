from rolepermissions.mixins import HasRoleMixin
from django.views.generic import ListView
from especialidades.models import PacienteEspecialidade
from transportes.models import PassageiroViagem
from django.db.models import Q


class PacienteViagemSearchView(HasRoleMixin,ListView):
   
    model = PassageiroViagem
    template_name = 'viagem/buscar_paciente_viagem.html'
    paginate_by = 10
    pk_url_kwarg = 'id'
    allowed_roles=['recepcao','regulacao','secretario','coordenador','acs']

    def get_queryset(self):
        buscar = self.request.GET.get('buscar', None)
        queryset = PassageiroViagem.objects.select_related(
            'paciente','viagem').all().order_by('-viagem')

        if buscar:
            buscar=buscar.rstrip()
            queryset = queryset.filter(
                Q(paciente__nome_completo__unaccent__icontains=buscar) | Q(paciente__cpf__icontains=buscar)
            )
            
        return queryset