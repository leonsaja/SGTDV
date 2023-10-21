from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q

from despesas.forms.reembolso_form import ReembolFormSet
from despesas.models import Diaria, Reembolso
from django.contrib.messages import constants
from django.contrib import messages


def reembolso_create(request,id):
    diaria=get_object_or_404(Diaria,id=id)

    if not diaria:
        return Http404()
    
    if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
            formset.save()
            messages.add_message(request,constants.SUCCESS,'cadastro realizado com sucesso')
            return redirect('despesas:list-reembolso')

    formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
    return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

def reembolso_update(request, id):
   diaria=get_object_or_404(Diaria,id=id)
    
   if not diaria:
        return Http404()
    
   if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('despesas:list-reembolso')
        

   formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

class ReembolsoListView(ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   queryset=Diaria.objects.select_related('profissional').filter(reembolso=1)
   ordering='-created_at'
   paginate_by=10
   
class SearchReembolsoListView(ListView):
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   paginate_by=10
   
   def get_queryset(self, *args, **kwargs):
        qs = super(SearchReembolsoListView,self).get_queryset(*args, **kwargs)
        buscar=self.request.GET.get('buscar',None)
        data=self.request.GET.get('data',None)
        
        if buscar and data:
            qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar))\
                    .filter(data_diaria__iexact=data).order_by('-created_at')
        
        elif buscar:
            qs=qs.select_related('profissional').filter(reembolso=1)\
                .filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar))\
                    .order_by('-created_at')
      
        elif data:
             qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(data_diaria__iexact=data).order_by('-created_at')
            
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

def reembolso_pdf(request,id):

    diaria=get_object_or_404(Diaria,id=id)
    context={}
    context['diaria']=diaria
    context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
    response = HttpResponse(content_type='application/pdf')

    
    context['movimentacao']=Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id).filter(Q(movimentacao=1)|Q(movimentacao=2)|Q(movimentacao=3)|Q(movimentacao=4)|Q(movimentacao=5)|Q(movimentacao=6)).exists()
    html_string = render_to_string('reembolso/pdf_reembolso.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
    
   