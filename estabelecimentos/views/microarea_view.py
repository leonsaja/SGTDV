from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..forms.form_microare import MicroAreaForm
from ..models import Estabelecimento, MicroArea


class MicroAreaCreateView(CreateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')

class MicroAreaUpdateView(UpdateView):
    model=MicroArea
    form_class=MicroAreaForm
    context_object_name='form'
    template_name='microarea/form_microarea.html'
    success_url=reverse_lazy('estabelecimentos:list-microarea')

class MicroAreaListView(ListView):
    model=MicroArea
    context_object_name='microareas'
    template_name='microarea/list_microarea.html'
   
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
       
        qs = qs.select_related('estabelecimento').order_by('id')
        return qs
   
class MicroAreaDetailView(DetailView):
    model=MicroArea
    context_object_name='microarea'
    template_name='microarea/detail_microarea.html'

class MicroAreaDeleteView(DeleteView):
    model=MicroArea
    context_object_name='form'
    success_url=reverse_lazy('estabelecimentos:list-microarea')
