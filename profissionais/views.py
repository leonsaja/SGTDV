
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
import re
from dal import autocomplete
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ProfissionalCreateView(SuccessMessageMixin,CreateView):
    
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Cadastro realizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ProfissionalUpdateView(SuccessMessageMixin,UpdateView):
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Dados atualizados com sucesso'
   
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ProfissionalDetailView(DetailView):

    model=Profissional
    template_name='profissional/detail_profissional.html'
    context_object_name='profissional'
 
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ProfissionalListView(ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10
    ordering='nome_completo'
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','digitador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ProfissionalSearchListView(ListView):

    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(ProfissionalSearchListView,self).get_queryset(*args, **kwargs)
        qs.select_related('estabelecimento').all()
        search_nome_cpf=self.request.GET.get('search_nome_cpf', '').strip()
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)
        
        if search_nome_cpf:
            qs=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
          
        if search_dt_nascimento:
             qs=qs.select_related('estabelecimento').filter(dt_nascimento__iexact=search_dt_nascimento)
        
        qs=qs.order_by('nome_completo')
        
        return qs

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
class ProfissionalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not self.request.user.is_authenticated:
            return Profissional.objects.none()

        qs = Profissional.objects.select_related('estabelecimento').all()
        
        if self.q:
            cpf_cns_limpo = re.sub(r'\D', '', self.q)

            if len(cpf_cns_limpo) == 11:
                qs = qs.filter(cpf=cpf_cns_limpo)
            elif len(cpf_cns_limpo) == 15:
                qs = qs.filter(cns=cpf_cns_limpo)
            else:
                self.q=self.q.rstrip()
                qs = qs.filter(nome_completo__unaccent__icontains=self.q)
                
        return qs

@login_required
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