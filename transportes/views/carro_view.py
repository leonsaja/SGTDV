from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.db.models import ProtectedError
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

def carroDelete(request, id):

    carro=get_object_or_404(Carro,id=id)
    
    try:
        carro.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('transportes:list-carro')

