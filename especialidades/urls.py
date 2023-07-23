from django.urls import path

from especialidades.views import \
    paciente_especialidade_view as view_paciente_especialidade

from .views import especialidade_view as view_especialidade

app_name='especialidades'

urlpatterns = [
    
    #Especialidades
    path('create/especialidade/',  view_especialidade.EspecialidadeCreateView.as_view(), name='add-especialidade' ),  
    path('update/<int:pk>/especialidade/',  view_especialidade.EspecialidadeUpdateView.as_view(), name='edit-especialidade' ),  
    path('list/especialidades/',  view_especialidade.EspecialidadeListView.as_view(), name='list-especialidade' ),  
    path('detail/<int:pk>/especialidade/',  view_especialidade.EspecialidadeDetailView.as_view(), name='detail-especialidade' ),  
    path('delete/<int:id>/especialidade/',  view_especialidade.especialidadeDelete, name='del-especialidade' ),  


    #Paciente Especialidade
    path('<int:id>/create/paciente_especialidade', view_paciente_especialidade.pacienteEspecialidadeCreate, name='add-paciente-especialidade' ),  
    path('update/<int:id>/paciente_especialidade', view_paciente_especialidade.pacienteEspecialidadeUpdate, name='edit-paciente-especialidade' ),  
    path('list/<int:id>/pacientes_especialidades', view_paciente_especialidade.pacienteEspecialidadeList, name='list-paciente-especialidade' ),
    path('search/<int:id>/pacientes_especialidades', view_paciente_especialidade.pacienteEspecialidadeSearch, name='search-paciente-especialidade'),
    path('detail /<int:pk>/paciente_especialidade', view_paciente_especialidade.PacienteEspecialidadeDetailView.as_view(), name='detail-paciente-especialidade' ),  
    path('delete/<int:id>/paciente_especialidade', view_paciente_especialidade.pacienteEspecialidadeDelete, name='del-paciente-especialidade' ),  

]   