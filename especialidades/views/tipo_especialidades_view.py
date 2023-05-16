from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView,CreateView,UpdateView
from especialidades.models import Especialidade
from especialidades.forms.form_tipoespecialidades import TipoEspeciedadesForm


class TipoEspecialidadeCreateView(CreateView):
    model=Especialidade
    form_class=TipoEspeciedadesForm
    template_name='tipoespecialidades/form_tipoespecialidade.html'
    context_object_name='form'
    