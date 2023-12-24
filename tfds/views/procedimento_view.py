from django.urls import reverse_lazy
from django.db.models import ProtectedError, Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import  UpdateView, ListView,CreateView,DetailView
from tfds.forms.form_procedimento import CodigoSiaForm
from tfds.models import CodigoSIA
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.messages import constants
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator

class ProcedimentoCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')
    success_message='Cadastrado com sucesso'
    allowed_roles=['coordenador','regulacao']  

class ProcedimentoUpdateView(HasRoleMixin, SuccessMessageMixin,UpdateView):
    model=CodigoSIA
    form_class=CodigoSiaForm
    template_name='procedimento/form_procedimento.html'
    context_object_name='form'
    success_url=reverse_lazy('tfds:list-procedimento')
    success_message='Dados atualizado com sucesso'
    allowed_roles=['coordenador','regulacao'] 

class ProcedimentosListView(HasRoleMixin,ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'
    ordering='-created_at'
    allowed_roles=['coordenador','regulacao','secretario']  

class ProcedimentoSearchListView(HasRoleMixin,ListView):
    model=CodigoSIA
    template_name='procedimento/list_procedimento.html'
    context_object_name='procedimentos'
    paginate_by=1
    allowed_roles=['coordenador','regulacao','secretario'] 
    
    def get_queryset(self,*args, **kwargs):
        qs= super(ProcedimentoSearchListView,self).get_queryset(*args, **kwargs)
        search_codigo=self.request.GET.get('search_codigo')
        
        if search_codigo:
            qs=qs.filter(codigo__icontains=search_codigo).order_by('-created_at')

        return qs
    
class ProcedimentosDetailView(HasRoleMixin,DetailView):
    model=CodigoSIA
    template_name='procedimento/detail_procedimento.html'
    context_object_name='procedimento'
    allowed_roles=['coordenador','regulacao','secretario'] 

has_role_decorator(['coordenador'])
def procedimentosDelete(request,id):
    
    codigo=get_object_or_404(CodigoSIA,id=id)

    try:
        codigo.delete()
        messages.add_message(request,constants.SUCCESS, "Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request,constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('tfds:list-procedimento')
    
    