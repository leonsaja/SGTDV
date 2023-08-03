from django.urls import path

from despesas.views import reembolso_view as reem_view

from relatorios.views import relatorioDiaria

app_name='relatorios'

urlpatterns = [
    
    #Diária
    path('diaria/relatorio',relatorioDiaria,name='relatorio-diaria'),
    
]
