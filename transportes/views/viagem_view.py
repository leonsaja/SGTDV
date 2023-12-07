

from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from weasyprint import HTML
from ..forms.viagem_form import PassageiroViagemSet, ViagemForm
from ..models import Viagem
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.messages import constants


def viagemCreate(request):
    viagem=Viagem()
    if request.method == 'POST':

        form = ViagemForm(request.POST,instance=viagem,prefix='viagem' )
        formset=PassageiroViagemSet(request.POST,instance=viagem,prefix='passageiro')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Viagem cadastrada com sucesso')
           
            return redirect('transportes:list-viagem')

    form = ViagemForm(request.POST or None,instance=viagem,prefix='viagem')
    formset=PassageiroViagemSet(request.POST or None,instance=viagem,prefix='passageiro')
    
    return render(request, 'viagem/form_viagem.html', {'form': form,'formset':formset})

def viagemUpdate(request,id):

    viagem=Viagem.objects.get(id=id)

    if not viagem:
        not Http404()

    if request.method == 'POST':

        form = ViagemForm(request.POST,instance=viagem,prefix='viagem' )
        formset=PassageiroViagemSet(request.POST,instance=viagem,prefix='passageiro')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('transportes:list-viagem')

    form = ViagemForm(request.POST or None,instance=viagem,prefix='viagem')
    formset=PassageiroViagemSet(request.POST or None,instance=viagem,prefix='passageiro')
    
    return render(request, 'viagem/form_viagem.html', {'form': form,'formset':formset})

class ViagemListView(ListView): 
    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs =super(ViagemListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('carro','motorista').order_by('-data_viagem')
        return qs
    
class ViagemSearchListView(ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(ViagemSearchListView,self).get_queryset(*args, **kwargs)
        
        destino_viagem=self.request.GET.get('destino_viagem',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        data=self.request.GET.get('data',None)

        if destino_viagem:
            qs=qs.select_related('motorista','carro').filter(destino_viagem__icontains=destino_viagem).order_by('-data_viagem')
                    
        if placa_carro:
            qs=qs.select_related('motorista','carro').filter(carro__placa__iexact=placa_carro).order_by('-data_viagem')
        
        if data :
             qs=qs.select_related('motorista','carro').filter(data_viagem__iexact=data).order_by('-data_viagem')
    
        return qs
    
class DetailViagemView(SuccessMessageMixin,DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viagem = Viagem.objects.select_related('motorista','carro').get(id=self.kwargs['pk']) 
        context['viagem']=viagem
        return context

class ViagemDeleteView(SuccessMessageMixin,DeleteView):

    model=Viagem
    success_url=reverse_lazy('transportes:list-viagem')
    success_message='Registro excluido com sucesso'
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

def viagemPdf(request,id):
    
    viagem=get_object_or_404(Viagem,id=id)
    response = HttpResponse(content_type='application/pdf')
    
    html_string = render_to_string('viagem/pdf_viagem.html',{'viagem':viagem})
    
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

   
    return response
