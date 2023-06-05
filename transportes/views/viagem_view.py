from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

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

class ListViagemView(ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.select_related('motorista','carro').all()
        return qs
    
class DetailViagemView(DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viagem"] = Viagem.objects.get(id=self.kwargs['pk']) 
        return context
    