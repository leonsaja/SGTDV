from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

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
        

   formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

class ReembolsoListView(ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   paginate_by=10


   def get_queryset(self, *args, **kwargs):
        qs = super(ReembolsoListView,self).get_queryset(*args, **kwargs)
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
        
        if search_nome_cpf and data:
            queryset=qs.select_related('profissional').filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=search_nome_cpf)| Q(profissional__cpf__icontains=search_nome_cpf)).filter(data_diaria__iexact=data).order_by('-data_diaria')
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('profissional').filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=search_nome_cpf)| Q(profissional__cpf__icontains=search_nome_cpf)).order_by('-data_diaria')
            return queryset
        
        elif data:
            queryset=qs.select_related('profissional').filter(reembolso=1).filter(data_diaria__iexact=data).order_by('-data_diaria')
            return queryset 
    
        qs = qs.select_related('profissional').filter(reembolso=1).order_by('-data_diaria')
        return qs
   
class ReembolsoDetailView(DetailView):
    model=Diaria
    template_name='reembolso/detail_reembolso.html'
   
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
    
        return context

class ReembolsoDeleteView(DeleteView):
   pass
