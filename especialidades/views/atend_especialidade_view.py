from especialidades.models import AtendimentoEspecialidade, PacienteSia,Especialidade,PacienteEspecialidade
from especialidades.forms.form_atendimento_especialidade import AtendimentoEspecialidadeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.messages import constants
from django.contrib.messages.views import SuccessMessageMixin
from especialidades.forms.form_paciente import AtendPacienteSet

def atend_especialidade_create(request,id):
    
    atend_especialidade=AtendimentoEspecialidade()
   
    if request.method == 'POST':

        form = AtendimentoEspecialidadeForm(request.POST,instance=atend_especialidade,prefix='atendimento' )
        formset=AtendPacienteSet(request.POST,instance=atend_especialidade,prefix='paciente')
        if form.is_valid() and formset.is_valid():
            
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso')
            return redirect('tfds:list-recibo_tfd')

    form = AtendimentoEspecialidadeForm(request.POST or None,instance=atend_especialidade,prefix='atendimento')
    formset=AtendPacienteSet(request.POST or None,instance=atend_especialidade,prefix='paciente')
    
    return render(request, 'atendimento_especialidade/form_atend_especialidade.html', {'form': form,'formset':formset})
