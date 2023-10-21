
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView,
                                  UpdateView)

from django.contrib.messages.views import SuccessMessageMixin

from especialidades.forms.form_especialidade import EspecialidadeForm
from especialidades.models import Especialidade, PacienteEspecialidade


class EspecialidadeCreateView(SuccessMessageMixin,CreateView):
    model=Especialidade
    form_class=EspecialidadeForm
    success_url=reverse_lazy('especialidades:list-especialidade')
    template_name='especialidade/form_especialidade.html' 
    context_object_name='form'
    success_message='Cadastro realizado com sucesso'

class EspecialidadeUpdateView(SuccessMessageMixin,UpdateView):
    model=Especialidade
    form_class=EspecialidadeForm
    template_name='especialidade/form_especialidade.html'
    success_url=reverse_lazy('especialidades:list-especialidade')
    context_object_name='form'
    success_message='Dados atualizado com sucesso'

class EspecialidadeListView(ListView):

    model=Especialidade
    template_name='especialidade/list_especialidades.html'
    context_object_name='especialidades'
    paginate_by=10

    def get_queryset(self):
        qs=super(EspecialidadeListView,self).get_queryset()
        buscar=self.request.GET.get('buscar',None)

        if buscar:
            queryset=qs.filter(nome__icontains=buscar).order_by('-nome')
            return queryset 

        qs=qs.all().order_by('nome')                                          
        
        return qs

def especialidadeDetail(request,id):
    context={}
    template='especialidade/detail_especialidade.html'
    
    especialidade=get_object_or_404(Especialidade,id=id)
    context['especialidade']=especialidade
    pacientes_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').filter(especialidade_id=especialidade.id)
    
    paginator = Paginator(pacientes_especialidade,10)  
    page_number = request.GET.get("page")
    context['page_obj']= paginator.get_page(page_number)
    return render(request,template, context)
     
def especialidadeDelete(request, id):
    especialidade=Especialidade.objects.get(id=id)
    
    if not especialidade:
        raise Http404()
    try:
        especialidade.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluido com sucesso')
        
    except ProtectedError:
        messages.add_message(request,constants.ERROR, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('especialidades:list-especialidade')
       
