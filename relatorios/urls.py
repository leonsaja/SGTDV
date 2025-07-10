 
from django.urls import path

from despesas.views import reembolso_view as reem_view
                           
from relatorios.views.diaria_view import relatorio_diaria
from relatorios.views.especialidade_view import relatorio_especialidade
from relatorios.views.paciente_especialidade_view import relatorio_pacientes_especialidade
from relatorios.views.recibo_tfd_view import relatorio_recibo_tfd
from relatorios.views.registro_transporte_view import relatorio_registro_transporte
from relatorios.views.recibo_passagem_view import relatorio_recibo_passagem
from relatorios.views.viagem_view import relatorio_viagem
from relatorios.views.atendimento_especialidade import relatorio_atendimento_especialidade
app_name='relatorios'

urlpatterns = [ 

    #Diária
    path('diaria/relatorio/',relatorio_diaria,name='relatorio-diaria'),

    #Especialidade
    path('especialidade/relatorio/',relatorio_especialidade,name='relatorio-especialidade'),
    
    #PacienteEspecialidade
    path('pacientes-especialidade/relatorio/',relatorio_pacientes_especialidade,name='relatorio-paciente-especialidade'),
    
    #Atendimento
    path('atendimento-especialidade/relatorio/',relatorio_atendimento_especialidade,name='relatorio-atendimento-especialidade'),

    #Recibo de Tfd
    path('recibo-tfd/relatorio/',relatorio_recibo_tfd,name='relatorio-recibo-tfd'),

    #Recibo de Passagem
    path('recibo-passagem/relatorio/',relatorio_recibo_passagem,name='relatorio-recibo-passagem'),
    
    #Registro de Transporte
    path('registro-transporte/relatorio/',relatorio_registro_transporte,name='relatorio-registro-transporte'),

    #Viagem
    path('viagem/relatorio/',relatorio_viagem,name='relatorio-viagem')
    
]

