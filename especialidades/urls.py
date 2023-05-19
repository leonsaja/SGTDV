from django.urls import path

from .views import tipo_especialidades_view as view_tipoespecialidade
from .views import especialidade_view as view_especialidade

app_name='especialidades'

urlpatterns = [
    
    #Tipo Especialidades
    path('create/tipoespecialidade/',  view_tipoespecialidade.TipoEspecialidadeCreateView.as_view(), name='add-tipoespecialidade' ),  
    path('update/<int:pk>/tipoespecialidade/',  view_tipoespecialidade.TipoEspecialidadeUpdateView.as_view(), name='edit-tipoespecialidade' ),  
    path('list/tipoespecialidades/',  view_tipoespecialidade.TipoEspecialidadeListView.as_view(), name='list-tipoespecialidade' ),  
    path('detail/<int:pk>/tipoespecialidade/',  view_tipoespecialidade.TipoEspecialidadeDetailView.as_view(), name='detail-tipoespecialidade' ),  


    #Especialidade
    path('create/<int:id>/paciente_especialidade/', view_especialidade.especialidadeCreate, name='add-paciente-especialidade' ),  
    path('update/<int:id>/paciente_especialidade/', view_especialidade.especialidadeUpdate, name='edit-paciente-especialidade' ),  
    path('list/<int:pk>/pacientes_especialidades/', view_especialidade.EspecialidadeListView.as_view(), name='list-paciente-especialidade' ),
    path('detail/<int:pk>/paciente_especialidade/', view_especialidade.EspecialidadeDetailView.as_view(), name='detail-paciente-especialidade' ),  

]   