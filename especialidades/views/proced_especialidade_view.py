
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
from especialidades.forms.form_proced_especialidade import ProcedEspecialidadeForm
from especialidades.models import ProcedimentosEspecialidade
from dal import autocomplete

class ProcedEspecialidadeCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    model=ProcedimentosEspecialidade
    form_class=ProcedEspecialidadeForm
    success_url=reverse_lazy('especialidades:list-proced_especialidade')
    template_name='procedimento_especialidade/form_proced_especialidade.html' 
    context_object_name='form'
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['regulacao','recepcao']

class ProcedEspecialidadeUpdateView(HasRoleMixin,SuccessMessageMixin,UpdateView):
    model=ProcedimentosEspecialidade
    form_class=ProcedEspecialidadeForm
    template_name='procedimento_especialidade/form_proced_especialidade.html'
    success_url=reverse_lazy('especialidades:list-proced_especialidade')
    context_object_name='form'
    success_message='Dados atualizado com sucesso'
    allowed_roles=['regulacao','recepcao']

class ProcedEspecialidadeListView(HasRoleMixin,ListView):

    model=ProcedimentosEspecialidade
    template_name='procedimento_especialidade/list_proced_especialidade.html'
    context_object_name='procedimentos'
    paginate_by=10
    allowed_roles=['regulacao','recepcao','secretario','coordenador']

    def get_queryset(self):
        qs=super(ProcedEspecialidadeListView,self).get_queryset()
        buscar=self.request.GET.get('buscar',None)

        if buscar:
            queryset=qs.filter(nome_procedimento__icontains=buscar).order_by('-nome_procedimento')
            return queryset 

        qs=qs.all().order_by('id')                                          
        
        return qs


class ProcedEspecialidadeDetail(HasRoleMixin,DetailView):
    model=ProcedimentosEspecialidade
    template_name='procedimento_especialidade/detail_proced_especialidade.html'
    context_object_name='procedimento'
    allowed_roles=['regulacao','recepcao','coordenador','secretario']
    
    
class ProcedimentoAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ProcedimentosEspecialidade.objects.none()
        
        qs = ProcedimentosEspecialidade.objects.all()
        
        if self.q:
            self.q=self.q.rstrip()
            qs = qs.filter(nome_procedimento__unaccent__icontains=self.q)

        return qs
    
@has_role_decorator(['coordenador'])
def especialidadeDelete(request, id):
    procedimento=ProcedimentosEspecialidade.objects.get(id=id)
    
    if not procedimento:
        raise Http404()
    try:
        procedimento.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluido com sucesso')
        
    except ProtectedError:
        messages.add_message(request,constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('especialidades:list-proced_especialidade')
       
