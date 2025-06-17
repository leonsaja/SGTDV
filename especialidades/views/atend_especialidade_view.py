from especialidades.models import AtendimentoEspecialidade, PacienteSia
from especialidades.forms.form_atendimento_especialidade import AtendimentoEspecialidadeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.messages import constants
from django.contrib.messages.views import SuccessMessageMixin
from especialidades.forms.form_atendimento_especialidade import AtendPacienteSet

def atendi_especialidade_create(request):
    atend_especialidade=AtendimentoEspecialidade()
    if request.method == 'POST':

        form = AtendimentoEspecialidadeForm(request.POST,instance=atend_especialidade,prefix='atendimento' )
        formset=PacienteSia(request.POST,instance=atend_especialidade,prefix='paciente')
        if form.is_valid() and formset.is_valid():
            
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso')
            return redirect('tfds:list-recibo_tfd')

    form = AtendimentoEspecialidadeForm(request.POST or None,instance=atend_especialidade,prefix='atendimento')
    formset=PacienteSia(request.POST or None,instance=atend_especialidade,prefix='paciente')
    
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})
