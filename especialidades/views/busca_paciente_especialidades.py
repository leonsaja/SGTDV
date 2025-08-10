from rolepermissions.mixins import HasRoleMixin
from django.views.generic import ListView
from especialidades.models import PacienteEspecialidade
from django.db.models import ProtectedError, Q
from cidadao.models import Cidadao
class PacienteEspecialidadeSearchView(HasRoleMixin,ListView):
   
    model = PacienteEspecialidade
    template_name = 'buscar_paciente_especialidade.html'
    paginate_by = 10
    pk_url_kwarg = 'id'
    allowed_roles=['recepcao','regulacao','secretario','coordenador','acs']

    def get_queryset(self):
        buscar = self.request.GET.get('buscar', None)
        queryset = PacienteEspecialidade.objects.select_related(
            'paciente', 'especialidade', 'procedimento').all()

        if buscar:
            buscar=buscar.rstrip()
            queryset = queryset.filter(
                Q(paciente__nome_completo__icontains=buscar) | Q(paciente__cpf__icontains=buscar)
            )

    
            
            print('queryset',queryset)
            
        return queryset