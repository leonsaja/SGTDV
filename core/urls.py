from django.urls import path

from core.views import home
app_name='core'
from core.views import page_not_found_view
urlpatterns = [
   path('',home,name='home'),
   #path('calendario/', calendario_view, name='calendario'),
   #path('agendamentos_json/',agendamentos_json, name='agendamentos_json'),
   #path('agendamento/criar/', agendamento_criar_ajax, name='agendamento_criar_ajax'),
]
handler404 = 'core.views.page_not_found_view'