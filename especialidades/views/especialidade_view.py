
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from especialidades.forms.form_especialidade import EspecialidadeForm
from especialidades.models import Especialidade, PacienteEspecialidade


class EspecialidadeCreateView(CreateView):
    model=Especialidade
    form_class=EspecialidadeForm
    success_url=reverse_lazy('especialidades:list-especialidade')
    template_name='especialidade/form_especialidade.html'
    
    context_object_name='form'

class EspecialidadeUpdateView(UpdateView):
    model=Especialidade
    form_class=EspecialidadeForm
    template_name='especialidade/form_especialidade.html'
    success_url=reverse_lazy('especialidades:list-especialidade')
    context_object_name='form'

class EspecialidadeListView(ListView):
    model=Especialidade
    template_name='especialidade/list_especialidades.html'
    context_object_name='especialidades'
    paginate_by=5    

    def get_queryset(self):
        qs=super(EspecialidadeListView,self).get_queryset()
        busca_nome=self.request.GET.get('busca_nome',None)

        if busca_nome:
            queryset=qs.filter(nome__icontains=busca_nome).order_by('-nome')
            return queryset 

        qs=qs.all()                                                       
        return qs
    

class EspecialidadeDetailView(DetailView):
    model=Especialidade
    template_name='especialidade/detail_especialidade.html'
   

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        especialidade=Especialidade.objects.get(id=self.kwargs['pk'])
        context['especialidade']=especialidade
        return context
    

def especialidadeDelete(request, id):
    especialidade=Especialidade.objects.get(id=id)
    
    if not especialidade:
        raise Http404()
    try:
        especialidade.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('especialidades:list-especialidade')
       
