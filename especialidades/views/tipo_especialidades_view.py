
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from especialidades.forms.form_tipoespecialidades import TipoEspeciedadesForm
from especialidades.models import TipoEspecialidade


class TipoEspecialidadeCreateView(CreateView):
    model=TipoEspecialidade
    form_class=TipoEspeciedadesForm
    success_url=reverse_lazy('especialidades:list-tipoespecialidade')
    template_name='tipoespecialidade/form_tipoespecialidade.html'
    
    context_object_name='form'

class TipoEspecialidadeUpdateView(UpdateView):
    model=TipoEspecialidade
    form_class=TipoEspeciedadesForm
    template_name='tipoespecialidade/form_tipoespecialidade.html'
    success_url=reverse_lazy('especialidades:list-tipoespecialidade')
    context_object_name='form'

class TipoEspecialidadeListView(ListView):
    model=TipoEspecialidade
    template_name='tipoespecialidade/list_tipoespecialidades.html'
    context_object_name='tipoespecialidades'

class TipoEspecialidadeDetailView(DetailView):
    model=TipoEspecialidade
    template_name='tipoespecialidade/detail_tipoespecialidade.html'
    context_object_name='tipoespecialidade'
    

class TipoEspecialidadeDeleteView(DeleteView):
    model=TipoEspecialidade
    success_url=reverse_lazy('especialidades:list-tipoespecialidade')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)
       
