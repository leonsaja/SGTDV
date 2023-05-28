
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from despesas.forms.diaria_form import DiariaForm
from despesas.forms.reembolso_form import ReembolFormSet

from ..models import Diaria, Reembolso


class DiariaCreateView(CreateView):
   model=Diaria
   form_class=DiariaForm 
   template_name='diaria/form_diaria.html'
   success_url=reverse_lazy('despesas:list-diaria')

class DiariaUpdateView(UpdateView):

    model=Diaria
    form_class=DiariaForm
    template_name='diaria/form_diaria.html'
    success_url=reverse_lazy('despesas:list-diaria')

class DiariaListView(ListView):
    model=Diaria
    template_name='diaria/list_diaria.html'
    context_object_name='diarias'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.select_related('profissional').all().order_by('profissional__nome_completo')
        return qs
    
class DiariaDetailView(DetailView):
    model=Diaria
    template_name='diaria/detail_diaria.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
        
        return context

def diariaDelete(request, id):
    diaria=Diaria.objects.get(id=id)

    if not diaria:
        return Http404()
    try:
        diaria.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('despesas:list-diaria')
    
