from django.shortcuts import render
from django.views.generic import CreateView
from transportes.models import RegistroTransporte
from transportes.forms.registro_transporte_form import RegistroTransporteForm
class RegistroTransporteCreateView(CreateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/create_registro_transporte.html'
    context_object_name='form'
    