from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from ..models import ReciboPassagemTFD


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
    context_object_name='recibos'