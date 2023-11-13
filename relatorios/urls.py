 
from django.urls import path

from despesas.views import reembolso_view as reem_view
from relatorios.views.views_geral import (relatorioDiaria, relatorio_diaria_pdf,
                              relatorioReciboTfdPdf, relatorioReembolsoPdf)
from relatorios.views.diaria_views import relatorio_diaria
app_name='relatorios'

urlpatterns = [ 

    #Diária
    path('diaria/relatorio/',relatorio_diaria,name='relatorio-diaria'),
    path('diaria/relatorio-diaria-pdf/',relatorio_diaria_pdf,name='relatorio-diaria-pdf'),

    #Reembolso
    path('reembolso/<int:id>/relatorio-reembolso',relatorioReembolsoPdf,name='relatorio-reembolso-pdf'),

    #TFD RECIBOS DE TFD
    path('recibo-tfd/<int:id>/relatorio-recibo-tfd',relatorioReciboTfdPdf,name='relatorio-recibo-tfd-pdf'),


]

