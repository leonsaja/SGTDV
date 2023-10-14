from django.urls import reverse_lazy
from django.views.generic import  UpdateView, ListView,CreateView
from tfds.forms.form_procedimento import CodigoSiaForm
from tfds.models import CodigoSIA



class ProcedimentoCreateView(CreateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')
    
class ProcedimentoUpdateView(UpdateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')

class ProcedimentosListView(ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'