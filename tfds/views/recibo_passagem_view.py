from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from tfds.forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from tfds.models import ReciboPassagemTFD


class ReciboPassagemTFDCreateView(CreateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')

class ReciboPassagemTFDUpdateView(UpdateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')


class ListReciboPassagemTFDView(ListView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibos"] =ReciboPassagemTFD.objects.select_related('paciente', 'acompanhante').all()
        return context
    

class DetailReciboPassagemTFD(DetailView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/detail_recibo_passagem.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibo"] =ReciboPassagemTFD.objects.select_related('paciente', 'acompanhante').get(id=self.kwargs['pk'])
       
        return context
    



     
                                                                                                                                                                                                                                              
