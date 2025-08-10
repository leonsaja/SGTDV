
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from ..forms.form_microare import MicroAreaForm
from ..models import  MicroArea
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.mixins import HasRoleMixin

class MicroAreaCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['coordenador']

class MicroAreaUpdateView(HasRoleMixin,SuccessMessageMixin,UpdateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message='Dados atualizado com sucesso'
    allowed_roles=['coordenador']

class MicroAreaListView(HasRoleMixin,ListView):
    model=MicroArea
    context_object_name='microareas'
    template_name='microarea/list_microarea.html'
    queryset=MicroArea.objects.select_related('estabelecimento').all()
    allowed_roles=['coordenador','secretario']

class MicroAreaDetailView(DetailView):
    model=MicroArea
    context_object_name='microarea'
    template_name='microarea/detail_microarea.html'
    allowed_roles=['coordenador','secretario']

class MicroAreaDeleteView(HasRoleMixin,SuccessMessageMixin,DeleteView):
    model=MicroArea
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
    success_message="Registro excluido com sucesso"
    allowed_roles=['coordenador']

