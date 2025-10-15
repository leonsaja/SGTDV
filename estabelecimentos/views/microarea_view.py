from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from ..forms.form_microare import MicroAreaForm
from ..models import  MicroArea
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class MicroAreaCreateView(SuccessMessageMixin,CreateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message='Cadastro realizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class MicroAreaUpdateView(SuccessMessageMixin,UpdateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message='Dados atualizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class MicroAreaListView(ListView):
    model=MicroArea
    context_object_name='microareas'
    template_name='microarea/list_microarea.html'
    queryset=MicroArea.objects.select_related('estabelecimento').all()

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class MicroAreaDetailView(DetailView):
    model=MicroArea
    context_object_name='microarea'
    template_name='microarea/detail_microarea.html'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class MicroAreaDeleteView(SuccessMessageMixin,DeleteView):
    model=MicroArea
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message="Registro excluido com sucesso"

