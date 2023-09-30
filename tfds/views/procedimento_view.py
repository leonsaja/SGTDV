
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, UpdateView, ListView,CreateView
from tfds.forms.form_tfd import CodigoSiaForm
from tfds.models import CodigoSIA, ReciboTFD
from django.http import HttpResponse


class ProcedimentoCreateView(CreateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'

class ProcedimentoView(UpdateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'

class ProcedimentosListView(ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'