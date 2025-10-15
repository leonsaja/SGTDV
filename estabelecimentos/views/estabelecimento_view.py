from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,UpdateView)
from django.contrib.messages import constants
from django.contrib import messages
from django.db.models import ProtectedError
from ..forms.form_estabelecimento import EstabelecimentoForm
from ..models import Estabelecimento
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class EstabelecimentoCreateView(SuccessMessageMixin,CreateView):
    model=Estabelecimento
    form_class=EstabelecimentoForm
    context_object_name='form'
    template_name='estabelecimento/form_estabelecimento.html'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    success_message='Cadastro realizado com sucesso'
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class EstabelecimentoUpdateView(SuccessMessageMixin,UpdateView):
   
    model=Estabelecimento
    form_class=EstabelecimentoForm
    template_name='estabelecimento/form_estabelecimento.html'
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-estabelecimento')
    success_message='Dados atualizado com  sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')      
class EstabelecimentoDetailView(DetailView):
    model=Estabelecimento
    template_name='estabelecimento/detail_estabelecimento.html'
    context_object_name='estabelecimento'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')     
class EstabelecimentoListView(ListView):
    model=Estabelecimento
    template_name='estabelecimento/list_estabelecimento.html'
    context_object_name='estabelecimentos'
    paginate_by=10
    ordering='nome'

@login_required
@has_role_decorator(['coordenador'])                                                                                                                                                                                                            
def estabelecimento_delete(request,id):
   
    estabelecimento=get_object_or_404(Estabelecimento,id=id)

    try:
        estabelecimento.delete()
        messages.add_message(request, constants.SUCCESS ,"Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request, constants.ERROR ,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('estabelecimentos:list-estabelecimento')
