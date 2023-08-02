from django.urls import path

from despesas.views import reembolso_view as reem_view

from .views import diaria_view as diaria_view

app_name='relatorios'

urlpatterns = [
    
    #Diária
    path('diaria/relatorio',diaria_view.DiariaListView.as_view(),name='relatorio-diaria'),
    
]
