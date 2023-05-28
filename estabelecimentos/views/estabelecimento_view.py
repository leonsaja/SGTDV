from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from profissionais.models import Profissional

from ..forms.form_estabelecimento import EstabelecimentoForm
from ..models import Estabelecimento


class EstabelecimentoCreateView(CreateView):
    model=Estabelecimento
    form_class=EstabelecimentoForm
    context_object_name='form'
    template_name='estabelecimento/form_estabelecimento.html'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    
    
class EstabelecimentoUpdateView(UpdateView):
   
    model=Estabelecimento
    form_class=EstabelecimentoForm
    template_name='estabelecimento/form_estabelecimento.html'
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    
    
class EstabelecimentoDetailView(DetailView):
    model=Estabelecimento
    template_name='estabelecimento/detail_estabelecimento.html'
    context_object_name='estabelecimento'

    
class EstabelecimentoListView(ListView):
    model=Estabelecimento
    template_name='estabelecimento/list_estabelecimento.html'
    context_object_name='estabelecimentos'
    

                                                                                                                                                                                                                                                                         
class EstabelecimentoDeleteView(DeleteView):
    model=Estabelecimento
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        