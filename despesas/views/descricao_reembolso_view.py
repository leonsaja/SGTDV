from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView,UpdateView,DetailView)
from rolepermissions.mixins import HasRoleMixin
from django.contrib.messages.views import SuccessMessageMixin
from despesas.models import DescricaoReembolso
from despesas.forms.descricao_reembolso_form import DescricaoReembolsoForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rolepermissions.decorators import has_role_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DescricaoReembolsoCreateView(SuccessMessageMixin,CreateView):
    model=DescricaoReembolso
    form_class=DescricaoReembolsoForm
    success_url=reverse_lazy('despesas:list-descricao-reembolso')
    template_name='descricao_reembolso/form_descricao_reembolso.html' 
    context_object_name='form'
    success_message='Cadastro realizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DescricaoReembolsoUpdateView(SuccessMessageMixin,UpdateView):
    model=DescricaoReembolso
    form_class=DescricaoReembolsoForm
    template_name='descricao_reembolso/form_descricao_reembolso.html' 
    success_url=reverse_lazy('despesas:list-descricao-reembolso')
    context_object_name='form'
    success_message='Dados atualizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DescricaoReembolsoListView(ListView):

    model=DescricaoReembolso
    template_name='descricao_reembolso/list_descricao_reembolso.html' 
    context_object_name='descricoes'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DescricaoReembolsoDetaiView(DetailView):
    
    model=DescricaoReembolso
    template_name='descricao_reembolso/detail_descricao_reembolso.html' 
    context_object_name='descricao'
    