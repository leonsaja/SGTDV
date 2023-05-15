from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..forms.form_estabelecimento import EstabelecimentoForm
from ..models import Estabelecimento


class EstabelecimentoCreateView(CreateView):
    model=Estabelecimento
    form_class=EstabelecimentoForm
    context_object_name='form'
    template_name='estabelecimento/form_estabelecimento.html'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    
    def get_context_data(self, *args, **kwargs):
        conext= super().get_context_data(*args, **kwargs)
        conext['title']='Cadasto de Estabelecimento'
        return conext

class EstabelecimentoUpdateView(UpdateView):
   
    model=Estabelecimento
    form_class=EstabelecimentoForm
    template_name='estabelecimento/form_estabelecimento.html'
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    
    def get_context_data(self, *args, **kwargs):
        conext= super().get_context_data(*args, **kwargs)
        conext['title']='Edição de Estabelecimentos'
        return conext
    
class EstabelecimentoDetailView(DetailView):
    model=Estabelecimento
    template_name='estabelecimento/detail_estabelecimento.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context={
            'title':'Estabelecimento',
            'estabelecimento':Estabelecimento.objects.get(id=self.kwargs['pk']),
        }
        return context

    
class EstabelecimentoListView(ListView):
    model=Estabelecimento
    template_name='estabelecimento/list_estabelecimento.html'
    context_object_name='estabelecimentos'
    
    
    def get_context_data(self, *args, **kwargs):
        conext= super().get_context_data(*args, **kwargs)
        conext['title']='Estabelecimentos'
        return conext

                                                                                                                                                                                                                                                                         
class EstabelecimentoDeleteView(DeleteView):
    model=Estabelecimento
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        