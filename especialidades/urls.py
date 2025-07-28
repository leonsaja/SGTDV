from django.urls import path

from especialidades.views import \
    paciente_especialidade_view as view_paciente_especialidade

from .views import especialidade_view as view_especialidade
from especialidades.views import atend_especialidade_view 
from especialidades.views import proced_especialidade_view as view_procedimento

app_name='especialidades'

urlpatterns = [
    
    #Especialidades
    path('create/especialidade/',  view_especialidade.EspecialidadeCreateView.as_view(), name='add-especialidade' ),  
    path('update/<int:pk>/especialidade/',  view_especialidade.EspecialidadeUpdateView.as_view(), name='edit-especialidade' ),  
    path('list/especialidades/',  view_especialidade.EspecialidadeListView.as_view(), name='list-especialidade' ),  
    path('detail/<int:pk>/especialidade/',  view_especialidade.especialidadeDetail, name='detail-especialidade' ),  
    path('delete/<int:id>/especialidade/',  view_especialidade.especialidadeDelete, name='del-especialidade' ),  


    #Paciente Especialidade
    path('<int:id>/create/paciente_especialidade', view_paciente_especialidade.PacienteEspecialidadeCreateView.as_view(), name='add-paciente-especialidade'),  
    path('update/<int:id>/paciente_especialidade', view_paciente_especialidade.PacienteEspecialidadeUpdateView.as_view(), name='edit-paciente-especialidade'),  
    path('<int:id>/search/pacientes_especialidades', view_paciente_especialidade.PacienteEspecialidadeListView.as_view(), name='search-paciente-especialidade'),
    path('detail /<int:pk>/paciente_especialidade', view_paciente_especialidade.PacienteEspecialidadeDetailView.as_view(), name='detail-paciente-especialidade' ),  
    path('delete/<int:id>/paciente_especialidade', view_paciente_especialidade.pacienteEspecialidade_delete, name='del-paciente-especialidade' ),  



    #Atendimento Paciente especialidade

    path('create/atendimento', atend_especialidade_view.atend_especialidade_create, name='add-atend_especialidade' ),
    path('update/<int:id>/atendimento', atend_especialidade_view.atend_especialidade_update, name='edit-atend_especialidade' ),
    path('list/atendimentos', atend_especialidade_view.AtendEspecialidadeListView.as_view(), name='list-atend_especialidade' ),
    path('detail/<int:pk>/atendimento', atend_especialidade_view.AtendEspecialidadeDetailView.as_view(), name='detail-atend_especialidade' ),
    path('delete/<int:pk>/atendimento', atend_especialidade_view.AtendEspecialidadeDeleteView.as_view(), name='del-atend-especialidade' ),  
    path("pdf/<int:id>/atendimento",atend_especialidade_view.atend_especialidade_pdf,name='pdf-atend_especialidade'),
    path('load-pacientes-by-especialidade/', atend_especialidade_view.load_pacientes_by_especialidade, name='load_pacientes_by_especialidade'),
   

    #Procedimento de Especialidades

    path('create/procedimento', view_procedimento.ProcedEspecialidadeCreateView.as_view(), name='add-proced_especialidade' ),
    path('update/<int:pk>/procedimento',view_procedimento.ProcedEspecialidadeUpdateView .as_view(), name='edit-proced_especialidade' ),
    path('list/procedimentos/',view_procedimento.ProcedEspecialidadeListView .as_view(), name='list-proced_especialidade' ),
    path('detail/<int:pk>/procedimento',view_procedimento.ProcedEspecialidadeDetail .as_view(), name='detail-proced_especialidade' ),
    path('delete/<int:id>/procedimento/',  view_procedimento.especialidadeDelete, name='del-proced_especialidade' ),  
    

]   