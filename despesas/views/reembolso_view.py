from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from despesas.forms.reembolso_form import ReembolFormSet
from despesas.models import Diaria, Reembolso


def reembolsoCreate(request,id):
    diaria=Diaria.objects.get(id=id)

    if not diaria:
        return Http404()
    
    if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
            formset.save()
            return redirect('despesas:list-diaria')

    formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
    return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

def reembolsoUpdate(request, id):
   diaria=Diaria.objects.get(id=id)
    
   if not diaria:
        return Http404()
    
   if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
            formset.save()
            return redirect('despesas:list-diaria')
        print('erros',formset.non_form_errors)

   formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

class ReembolsoListView(ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'

   def get_context_data(self,*args, **kwargs):
      context= super().get_context_data(*args, **kwargs)
      context={
         'Diarias':Diaria.objects.select_related('profissional').filter(reembolso=1),
      }
      return context

class ReembolsoDetailView(DetailView):
    model=Diaria
    template_name='reembolso/detail_reembolso.html'
   
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
       
        context={
            'diaria':Diaria.objects.select_related('profissional').get(id=self.kwargs['pk']),
        }
        return context


class ReembolsoDeleteView(DeleteView):
   pass
