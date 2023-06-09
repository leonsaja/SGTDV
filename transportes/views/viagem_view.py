from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms.viagem_form import PassageiroViagemSet, ViagemForm
from ..models import PassageiroViagem, Viagem


def viagemCreate(request):
    viagem=Viagem()
    if request.method == 'POST':

        form = ViagemForm(request.POST,instance=viagem,prefix='viagem' )
        formset=PassageiroViagemSet(request.POST,instance=viagem,prefix='passageiro')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
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
            return redirect('transportes:list-viagem')

    form = ViagemForm(request.POST or None,instance=viagem,prefix='viagem')
    formset=PassageiroViagemSet(request.POST or None,instance=viagem,prefix='passageiro')
    
    return render(request, 'viagem/form_viagem.html', {'form': form,'formset':formset})

class ViagemListView(ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'



    def get_queryset(self, *args, **kwargs):
        qs = super(ViagemListView,self).get_queryset(*args, **kwargs)
        
        destino_viagem=self.request.GET.get('destino_viagem',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        data=self.request.GET.get('data',None)


        if destino_viagem and data and placa_carro:
            queryset=qs.select_related('motorista','carro').filter(destino_viagem__icontains=destino_viagem).\
                filter(data_viagem__iexact=data).\
                    filter(carro__placa__iexact=placa_carro)
            return queryset
        
        elif destino_viagem and placa_carro:
            queryset=qs.select_related('motorista','carro').\
                filter(destino_viagem__icontains=destino_viagem).\
                filter(carro__placa__iexact=placa_carro)
            return queryset
        
        elif data and placa_carro:
            
             queryset=qs.select_related('motorista','carro').filter(data_viagem__iexact=data)\
             .filter(carro__placa__iexact=placa_carro)
             return queryset
        
        elif destino_viagem:
             queryset=qs.select_related('motorista','carro').\
                filter(destino_viagem__icontains=destino_viagem)
             return queryset
        
        elif data:
            queryset=qs.select_related('motorista','carro').filter(data_viagem__iexact=data)
            return queryset
        
        else:
            qs = qs.select_related('motorista','carro').order_by('-id')[:3]
            return qs
    """  def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.select_related('motorista','carro').all()
        return qs """
    
class DetailViagemView(DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viagem = Viagem.objects.select_related('motorista','carro').get(id=self.kwargs['pk']) 
        """ passageiros=PassageiroViagem.objects.select_related('viagem').filter(viagem__id=viagem.id) """
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