from typing import Any, Dict

from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from especialidades.forms.form_paciente_especialidade import \
    PacienteEspecialidadeForm
from especialidades.models import Especialidade, PacienteEspecialidade


def pacienteEspecialidadeCreate(request,id):
    especialidade=Especialidade.objects.get(id=id)

    if not especialidade:
        not Http404()

    if request.method == 'POST':
        form=PacienteEspecialidadeForm(request.POST)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=especialidade
            form.save()
            return redirect('especialidades:list-especialidade')

    
    form=PacienteEspecialidadeForm(request.POST or None)

    context={
            
            'form':form,
            'especialidade':especialidade
    } 
    return render(request,'paciente_especialidade/form_paciente_especialidade.html',context)

def pacienteEspecialidadeUpdate(request,id):
    paciente_especialidade=PacienteEspecialidade.objects.get(id=id)
    especialidade=Especialidade.objects.get(nome=paciente_especialidade.especialidade.nome)

    if not especialidade:
        not Http404()

    if request.method == 'POST':
        form=PacienteEspecialidadeForm(request.POST, instance=paciente_especialidade)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=especialidade
            form.save()
            return redirect('especialidades:detail-especialidade',especialidade.id)

    else:
        form=PacienteEspecialidadeForm(instance=paciente_especialidade)
    
    context={
            
            'form':form,
            'especialidade':especialidade,
    } 


    return render(request,'paciente_especialidade/form_paciente_especialidade.html',context)

def pacienteEspecialidadeDelete(request,id):

    paciente_especialidade=PacienteEspecialidade.objects.get(id=id)
    especialidade=Especialidade.objects.get(nome=paciente_especialidade.especialidade.nome)

    if not paciente_especialidade:
        raise Http404()
    try:
        paciente_especialidade.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('especialidades:detail-especialidade', especialidade.id)    

    
class PacienteEspecialidadeListView(ListView):
    
    model=PacienteEspecialidade
    template_name='paciente_especialidade/list_pacientes_especialidade.html'
    context_object_name='especialidades'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        especialidade=Especialidade.objects.get(id=self.kwargs['pk'])
        context['especialidade']=especialidade
        context['pacientes_especialidade']=PacienteEspecialidade.objects.select_related('paciente',\
                                             'especialidade','profissional').filter(especialidade__id=especialidade.id)

        return context

class PacienteEspecialidadeDetailView(DetailView):

    model=PacienteEspecialidade
    template_name='paciente_especialidade/detail_paciente_especialidade.html'
    context_object_name='especialidade'
    
    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        paciente_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').get(id=self.kwargs['pk'])
        context['paciente_especialidade']=paciente_especialidade
       
        return context
        


