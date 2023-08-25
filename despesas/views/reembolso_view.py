from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q

from despesas.forms.reembolso_form import ReembolFormSet
from despesas.models import Diaria, Reembolso


def reembolsoCreate(request,id):
    diaria=get_object_or_404(Diaria,id=id)

    if not diaria:
        return Http404()
    
    if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
            formset.save()
            return redirect('despesas:list-reembolso')

    formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
    return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

def reembolsoUpdate(request, id):
   diaria=get_object_or_404(Diaria,id=id)
    
   if not diaria:
        return Http404()
    
   if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=diaria,prefix='reembolso')
        if formset.is_valid():
           
            formset.save()
            return redirect('despesas:list-reembolso')
        

   formset=ReembolFormSet(request.POST or None,instance=diaria,prefix='reembolso')
    
   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset})

class ReembolsoListView(ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   paginate_by=10

   def get_queryset(self, *args, **kwargs):
        qs = super(ReembolsoListView,self).get_queryset(*args, **kwargs)
        qs = qs.select_related('profissional').filter(reembolso=1).order_by('-data_diaria')[:5]
        return qs

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
            queryset=qs.select_related('profissional')\
                .filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar))\
                    .filter(data_diaria__iexact=data).order_by('-data_diaria')
            return queryset
        
        elif buscar:
            queryset=qs.select_related('profissional').filter(reembolso=1)\
                .filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar))\
                    .order_by('-data_diaria')
            return queryset
        
        elif data:
            queryset=qs.select_related('profissional').filter(reembolso=1).filter(data_diaria__iexact=data).order_by('-data_diaria')
            return queryset 

class ReembolsoDetailView(DetailView):
    model=Diaria
    template_name='reembolso/detail_reembolso.html'
   
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
        
        return context


def reembolsoPdf(request,id):

    diaria=get_object_or_404(Diaria,id=id)
    context={}
    context['diaria']=diaria
    context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
    response = HttpResponse(content_type='application/pdf')

    
    context['movimentacao']=Reembolso.objects.select_related('diaria').filter(Q(movimentacao=1)|Q(movimentacao=2)|Q(movimentacao=3)|Q(movimentacao=4)|Q(movimentacao=5)|Q(movimentacao=6)).exists()
    html_string = render_to_string('reembolso/pdf_reembolso.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
    
   