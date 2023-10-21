from django.urls import reverse_lazy
from django.db.models import ProtectedError, Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import  UpdateView, ListView,CreateView,DetailView
from tfds.forms.form_procedimento import CodigoSiaForm
from tfds.models import CodigoSIA
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.messages import constants

class ProcedimentoCreateView(SuccessMessageMixin,CreateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')
    success_message='Cadastrado com sucesso'
    
class ProcedimentoUpdateView( SuccessMessageMixin,UpdateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')
    success_message='Dados atualizado com sucesso'

class ProcedimentosListView(ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'
    ordering='-created_at'
    
class ProcedimentoSearchListView(ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'
    paginate_by=1
    
    def get_queryset(self,*args, **kwargs):
        qs= super(ProcedimentoSearchListView,self).get_queryset(*args, **kwargs)
        search_codigo=self.request.GET.get('search_codigo')
        
        if search_codigo:
            qs=qs.filter(codigo__icontains=search_codigo).order_by('-created_at')

        return qs
    
class ProcedimentosDetailView(DetailView):
    model=CodigoSIA
    template_name='procedimento/detail_procedimento.html'
    context_object_name='procedimento'

def procedimentosDelete(request,id):
    
    
    codigo=get_object_or_404(CodigoSIA,id=id)

    try:
        codigo.delete()
        messages.add_message(request,constants.SUCCESS, "Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request,constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('tfds:list-procedimento')
    
    