
from django.db.models import ProtectedError, Q
from django.urls import reverse_lazy

from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView,CreateView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profissional
from despesas.models import Diaria
from profissionais.forms.form_profissional import ProfissionalForm
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator


class ProfissionalCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['coordenador','digitador']

class ProfissionalUpdateView(HasRoleMixin,SuccessMessageMixin,UpdateView):
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Dados atualizados com sucesso'
    allowed_roles=['coordenador','digitador']

class ProfissionalDetailView(HasRoleMixin,DetailView):

    model=Profissional
    template_name='profissional/detail_profissional.html'
    context_object_name='profissional'
    allowed_roles=['coordenador','digitador','secretario']

class ProfissionalListView(HasRoleMixin,ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10
    ordering='nome_completo'
    allowed_roles=['coordenador','digitador','secretario']
    
class ProfissionalSearchListView(HasRoleMixin,ListView):

    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10
    allowed_roles=['coordenador','digitador','secretario']


    def get_queryset(self, *args, **kwargs):
        qs = super(ProfissionalSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)
        
        if search_nome_cpf:
            qs=qs.select_related('estabelecimento').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
          
        if search_dt_nascimento:
             qs=qs.select_related('estabelecimento').filter(dt_nascimento__iexact=search_dt_nascimento)
        
        return qs

@has_role_decorator(['coordenador'])
def profissional_delete(request, id):
    profissional=get_object_or_404(Profissional,id=id)

    try:
        profissional.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluido com sucesso')
    except ProtectedError:
        messages.add_message(request, constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('profissionais:list-profissional')