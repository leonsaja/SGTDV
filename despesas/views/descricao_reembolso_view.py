
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView,UpdateView,DetailView)
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from django.contrib.messages.views import SuccessMessageMixin
from despesas.models import DescricaoReembolso
from despesas.forms.descricao_reembolso_form import DescricaoReembolsoForm

class DescricaoReembolsoCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    model=DescricaoReembolso
    form_class=DescricaoReembolsoForm
    success_url=reverse_lazy('despesas:list-descricao-reembolso')
    template_name='descricao_reembolso/form_descricao_reembolso.html' 
    context_object_name='form'
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['digitador']

class DescricaoReembolsoUpdateView(HasRoleMixin,SuccessMessageMixin,UpdateView):
    model=DescricaoReembolso
    form_class=DescricaoReembolsoForm
    template_name='descricao_reembolso/form_descricao_reembolso.html' 
    success_url=reverse_lazy('despesas:list-descricao-reembolso')
    context_object_name='form'
    success_message='Dados atualizado com sucesso'
    allowed_roles=['digitador']

class DescricaoReembolsoListView(HasRoleMixin,ListView):

    model=DescricaoReembolso
    template_name='descricao_reembolso/list_descricao_reembolso.html' 
    context_object_name='descricoes'
    allowed_roles=['digitador','secretario']


class DescricaoReembolsoDetaiView(HasRoleMixin,DetailView):
    
    model=DescricaoReembolso
    template_name='descricao_reembolso/detail_descricao_reembolso.html' 
    allowed_roles = ['digitador','secretario']
    context_object_name='descricao'
    