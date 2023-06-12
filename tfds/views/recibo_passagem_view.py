from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from tfds.forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from tfds.models import ReciboPassagemTFD


class ReciboPassagemTFDCreateView(CreateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'

class ReciboPassagemTFDUpdateView(UpdateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'

class ListReciboPassagemTFDView(ListView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibos"] =ReciboPassagemTFD.objects.select_related('paciente', 'acompanhante').all()
        print(context['recibos'])
        return context
    
    



     
                                                                                                                                                                                                                                              
