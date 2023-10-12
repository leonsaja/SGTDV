
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
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viagens"] = Viagem.objects.order_by('-data_viagem')[:10]
        return context
    
class ViagemSearchListView(ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=1

    def get_queryset(self, *args, **kwargs):
        qs = super(ViagemSearchListView,self).get_queryset(*args, **kwargs)
        
        destino_viagem=self.request.GET.get('destino_viagem',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        data=self.request.GET.get('data',None)

        if destino_viagem and data and placa_carro:
            queryset=qs.select_related('motorista','carro').filter(destino_viagem__icontains=destino_viagem).\
                filter(data_viagem__iexact=data).\
                    filter(carro__placa__iexact=placa_carro)
                    
        elif destino_viagem and placa_carro:
            queryset=qs.select_related('motorista','carro').\
                filter(destino_viagem__icontains=destino_viagem).\
                filter(carro__placa__iexact=placa_carro).order_by('-data_viagem')
        
        elif data and placa_carro:
            
             queryset=qs.select_related('motorista','carro').filter(data_viagem__iexact=data)\
             .filter(carro__placa__iexact=placa_carro).order_by('-data_viagem')
        
        elif destino_viagem:
             queryset=qs.select_related('motorista','carro').\
                filter(destino_viagem__icontains=destino_viagem).order_by('-data_viagem')
                
        elif data:
            queryset=qs.select_related('motorista','carro').filter(data_viagem__iexact=data).order_by('-data_viagem')
          
        
        elif placa_carro:
            queryset=qs.select_related('motorista','carro').\
            filter(carro__placa__iexact=placa_carro).order_by('-data_viagem')
       
        else:
            queryset=qs.select_related('motorista','carro').order_by('-data_viagem')
            
        return queryset
    
class DetailViagemView(SuccessMessageMixin,DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viagem = Viagem.objects.select_related('motorista','carro').get(id=self.kwargs['pk']) 
        context['viagem']=viagem
        return context

class ViagemDeleteView(DeleteView):

    model=Viagem
    success_url=reverse_lazy('transportes:list-viagem')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

    
    
    """ def viagemDelete(request,id):

    viagem=Viagem.objects.select_related('motorista','carro').get(id=id)
    
    if not viagem:
        raise Http404()
    try:
        viagem.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('profissionais:list-profissional') """
        
def viagemPdf(request,id):
    
    viagem=get_object_or_404(Viagem,id=id)
    response = HttpResponse(content_type='application/pdf')
    
    html_string = render_to_string('viagem/pdf_viagem.html',{'viagem':viagem})
    
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

   
    return response
