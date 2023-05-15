from audioop import reverse

from django.http import Http404
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from despesas.forms.diaria_form import DiariaForm
from despesas.forms.reembolso_form import ReembolFormSet

from ..models import Diaria


class DiariaCreateView(CreateView):
   model=Diaria
   form_class=DiariaForm 
   template_name='diaria/form_diaria.html'
   success_url=reverse_lazy('despesas:list-diaria')

class DiariaUpdateView(UpdateView):

    model=Diaria
    form_class=DiariaForm
    template_name='diaria/form_diaria.html'
    success_url=reverse_lazy('despesas:list-diaria')

class DiariaListView(ListView):
    model=Diaria
    template_name='diaria/list_diaria.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context={
            'title':'Diárias',
            'diarias':Diaria.objects.all(),            
        }
        return context
    
class DiariaDetailView(DetailView):
    model=Diaria
    template_name='diaria/detail_diaria.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context={
            'title':'Detalhe da Diária',
            'diaria':Diaria.objects.get(id=self.kwargs['pk']),
        }
        return context

class DiariaDeleteView(DeleteView):
    model=Diaria
    success_url=reverse_lazy('despesas:list-diaria')

    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)
    