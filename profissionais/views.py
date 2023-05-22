from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from profissionais.forms.form_profissional import (EnderecoForm,
                                                   ProfissionalForm)

from .models import Profissional


def profissionalCreate(request):
    if request.method == 'POST':
        form=ProfissionalForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
       
        if form.is_valid() and form_endereco.is_valid():
            
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            
            return redirect('profissionais:list-profissional')
        
    form=ProfissionalForm(request.POST or None)
    form_endereco=EnderecoForm(request.POST or None)
    
    return render(request,'profissional/form_profissional.html',{'form':form,'form_endereco':form_endereco})

def profissionalUpdate(request,id):
    profissional=Profissional.objects.get(id=id)
    
    if not profissional:
        raise Http404()

    if request.method == 'POST':
        form=ProfissionalForm(request.POST or None, instance=profissional)
        form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            return redirect('profissionais:list-profissional')
        
    form=ProfissionalForm(request.POST or None, instance=profissional)
    form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
    return render(request,'profissional/form_profissional.html',{'form':form,'endereco':form_endereco})

class ProfissionalListView(ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['profissionais']=Profissional.objects.all().order_by('-id')
        return context
    
    
class ProfissionalDetailView(DetailView):
    model=Profissional
    template_name='profissional/detail_profissional.html'
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['profissional']= Profissional.objects.get(pk=self.kwargs['pk'])
        
        return context
    
def profissionalDelete(request, id):
    profissional=Profissional.objects.get(id=id)

    if not profissional:
        raise Http404()
    try:
        profissional.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('profissionais:list-profissional')

class ProfissionalDiariaListView(ListView):
    model=Profissional
    template_name='profissional/diarias_profissional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profissional=Profissional.objects.get(pk=self.kwargs['pk'])
        context["diarias"] = profissional.profissionais.all()
        context['profissional']=profissional
        print(context['diarias'])
        return context
    
