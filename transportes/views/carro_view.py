from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms.carro_form import CarroForm
from ..models import Carro


class CarroCreateView(CreateView):

    model=Carro
    form_class=CarroForm
    template_name='carro/form_carro.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-carro')

class CarroUpdateView(UpdateView):  

    model=Carro
    form_class=CarroForm
    template_name='carro/form_carro.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-carro')

class ListCarroView(ListView):
    model=Carro
    template_name='carro/list_carros.html'
    context_object_name='carros'


class DetailCarraView(DetailView):
    model=Carro
    template_name='carro/detail_carro.html'
    context_object_name='carro'
