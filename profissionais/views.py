
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

class ProfissionalCreateView(SuccessMessageMixin,CreateView):
    
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Cadastro realizado com sucesso'
    
class ProfissionalUpdateView(SuccessMessageMixin,UpdateView):
    model=Profissional
    form_class=ProfissionalForm
    context_object_name='form'
    template_name='profissional/form_profissional.html'
    success_url=reverse_lazy('profissionais:list-profissional')
    success_message='Dados atualizados com sucesso'
 
def profissional_delete(request, id):
    profissional=get_object_or_404(Profissional,id=id)

    try:
        profissional.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluido com sucesso')
    except ProtectedError:
        messages.add_message(request, constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('profissionais:list-profissional')

class ProfissionalDetailView(DetailView):

    model=Profissional
    template_name='profissional/detail_profissional.html'
    context_object_name='profissional'

class ProfissionalListView(ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10
    ordering='-nome_completo'

class ProfissionalSearchListView(ListView):

    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(ProfissionalSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)
        
        
        if search_nome_cpf and search_dt_nascimento:
            qs=qs.select_related('estabelecimento','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(dt_nascimento__iexact=search_dt_nascimento)
          
        
        elif search_nome_cpf:
            qs=qs.select_related('estabelecimento','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
          
        
        elif search_dt_nascimento:
             qs=qs.select_related('estabelecimento','microarea').filter(dt_nascimento__iexact=search_dt_nascimento)
        
        return qs
