 
from django.urls import path

from despesas.views import reembolso_view as reem_view
                           
from relatorios.views.diaria_view import relatorio_diaria
from relatorios.views.especialidade_view import relatorio_especialidade
from relatorios.views.paciente_especialidade_view import relatorio_pacientes_especialidade
from relatorios.views.recibo_tfd_view import relatorio_recibo_tfd
app_name='relatorios'

urlpatterns = [ 

    #Diária
    path('diaria/relatorio/',relatorio_diaria,name='relatorio-diaria'),

    #Especialidade
    path('especialidade/relatorio/',relatorio_especialidade,name='relatorio-especialidade'),
    
    #PacienteEspecialidade
    path('pacientes-especialidade/relatorio/',relatorio_pacientes_especialidade,name='relatorio-paciente-especialidade'),

    #Recibo de Tfd
    path('recibo-tfd/relatorio/',relatorio_recibo_tfd,name='relatorio-recibo-tfd')
    
]

