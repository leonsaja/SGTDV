from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView
from transportes.models import RegistroTransporte
from transportes.forms.registro_transporte_form import RegistroTransporteForm


class RegistroTransporteCreateView(CreateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    
    
class RegistroTransporteUpdateView(UpdateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    
    
    
class RegistroTransporteListView(ListView):
    model =RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    
    
