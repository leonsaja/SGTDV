 
from django.urls import path

from despesas.views import reembolso_view as reem_view
from relatorios.views import (relatorioDiaria, relatorioDiariaPdf,
                              relatorioReciboTfdPdf, relatorioReembolsoPdf)

app_name='relatorios'

urlpatterns = [ 

    #Diária
    path('diaria/relatorio',relatorioDiaria,name='relatorio-diaria'),
    path('diaria/<int:id>/relatorio-diaria',relatorioDiariaPdf,name='relatorio-diaria-pdf'),


    #Reembolso
    path('reembolso/<int:id>/relatorio-reembolso',relatorioReembolsoPdf,name='relatorio-reembolso-pdf'),

    #TFD RECIBOS DE TFD
    path('recibo-tfd/<int:id>/relatorio-recibo-tfd',relatorioReciboTfdPdf,name='relatorio-recibo-tfd-pdf'),


]

