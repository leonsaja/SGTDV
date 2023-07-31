from typing import Any

from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from tfds.forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from tfds.models import ReciboPassagemTFD


class ReciboPassagemCreateView(CreateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')

class ReciboPassagemUpdateView(UpdateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')

class ReciboPassagemListView(ListView):

    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibos"] = ReciboPassagemTFD.objects.order_by('-data_recibo')[:10]
        return context
    
class ReciboPassagemSearchListView(ListView):
    
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'
    context_object_name='recibos'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboPassagemSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_data_recibo=self.request.GET.get('data',None)

        print('nome',search_nome_cpf)


        if search_nome_cpf and search_data_recibo:

            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
                .filter(data_recibo__iexact=search_data_recibo)
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))
            return queryset
        
        elif search_data_recibo:
             
             queryset=qs.select_related('paciente','acompanhante').filter(data_recibo__iexact=search_data_recibo)
             return queryset
        
class ReciboPassagemDetailView(DetailView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/detail_recibo_passagem.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibo"] =ReciboPassagemTFD.objects.select_related('paciente', 'acompanhante').get(id=self.kwargs['pk'])
       
        return context


class ReciboPassagemDeleteView(DeleteView):
    model=ReciboPassagemTFD
    success_url=reverse_lazy('tfds:list-recibo_passagem')

    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)

     
                                                                                                                                                                                                                                              
