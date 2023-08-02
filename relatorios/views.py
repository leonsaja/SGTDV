from django.shortcuts import render

from django.views.generic import ListView
from despesas.models import Diaria


class RelatorioDiariaListView(ListView):
    
    model=Diaria
    template_name='diarias/relatorio_diarias.html'
    
