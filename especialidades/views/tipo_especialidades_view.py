
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView,CreateView,UpdateView
from especialidades.models import TipoEspecialidade
from especialidades.forms.form_tipoespecialidades import TipoEspeciedadesForm


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
    


       
