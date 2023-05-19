from typing import Any, Dict
from django.http import Http404
from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from django.views.generic import DeleteView, DetailView, ListView,CreateView,UpdateView
from especialidades.models import Especialidade,TipoEspecialidade
from especialidades.forms.form_especialidade import EspecialidadeForm



def especialidadeCreate(request,id):
    especialidade=TipoEspecialidade.objects.get(id=id)

    if not especialidade:
        not Http404()

    if request.method == 'POST':
        form=EspecialidadeForm(request.POST)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=especialidade
            form.save()
            return redirect('especialidades:list-tipoespecialidade')

    
    form=EspecialidadeForm(request.POST or None)

    context={
            
            'form':form,
            'especialidade':especialidade
    } 
    return render(request,'especialidade/form_especialidade.html',context)

def especialidadeUpdate(request,id):
    especialidade=Especialidade.objects.get(id=id)
    tipoespecialidade=TipoEspecialidade.objects.get(nome=especialidade.especialidade.nome)

    if not especialidade:
        not Http404()

    if request.method == 'POST':
        form=EspecialidadeForm(request.POST, instance=especialidade)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=tipoespecialidade
            form.save()
            return redirect('especialidades:list-tipoespecialidade')

    else:
        form=EspecialidadeForm(instance=especialidade)
    
    context={
            
            'form':form,
            'especialidade':tipoespecialidade,
    } 


    return render(request,'especialidade/form_especialidade.html',context)


class EspecialidadeListView(ListView):
    
    model=Especialidade
    template_name='tipoespecialidade/detail_tipoespecialidade.html'
    context_object_name='especialidades'

class EspecialidadeDetailView(DetailView):

    model=Especialidade
    template_name='especialidade/detail_especialidade.html'
    context_object_name='especialidade'
    
    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        especialidade=Especialidade.objects.get(id=self.kwargs['pk'])
        context['tipoespecialidade']=TipoEspecialidade.objects.get(nome=especialidade.especialidade.nome)
        context['especialidade']=especialidade
       
        return context
        


