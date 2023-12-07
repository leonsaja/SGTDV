
from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, redirect, render
from especialidades.forms.form_paciente_especialidade import PacienteEspecialidadeForm
from especialidades.models import Especialidade, PacienteEspecialidade
from django.contrib import messages
from django.contrib.messages import constants
from django.views.generic import DetailView


def pacienteEspecialidade_create(request,id):
    
    especialidade=get_object_or_404(Especialidade,id=id)

    if request.method == 'POST':
        form=PacienteEspecialidadeForm(request.POST)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=especialidade
            form.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso')
            return redirect('especialidades:detail-especialidade', especialidade.id)

    
    form=PacienteEspecialidadeForm(request.POST or None)

    context={
            
            'form':form,
            'especialidade':especialidade
    } 
    return render(request,'paciente_especialidade/form_paciente_especialidade.html',context)

def pacienteEspecialidade_update(request,id):
    paciente_especialidade=get_object_or_404(PacienteEspecialidade,id=id)
  
    especialidade=Especialidade.objects.get(nome=paciente_especialidade.especialidade.nome)
   
    if request.method == 'POST':
        form=PacienteEspecialidadeForm(request.POST, instance=paciente_especialidade)

        if form.is_valid():
            form=form.save(commit=False)
            form.especialidade=especialidade
            form.save()
            messages.add_message(request,constants.SUCCESS,'Dados  atualizado com sucesso')
            return redirect('especialidades:detail-especialidade', especialidade.id)

    else:
        form=PacienteEspecialidadeForm(instance=paciente_especialidade)
    
    context={
            'form':form,
            'especialidade':especialidade,
    } 
    return render(request,'paciente_especialidade/form_paciente_especialidade.html',context)

def pacienteEspecialidade_delete(request,id):

    paciente_especialidade=get_object_or_404(PacienteEspecialidade,id=id)
    especialidade=Especialidade.objects.get(nome=paciente_especialidade.especialidade.nome)

    try:
        paciente_especialidade.delete()
        messages.add_message(request,constants.SUCCESS,'Registro excluido com sucesso')
    except ProtectedError:
        messages.add_message(request,constants.ERROR ,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('especialidades:detail-especialidade', especialidade.id)    

def pacienteEspecialidade_search(request,id):
    
    template_name='especialidade/detail_especialidade.html'
    context=[]

    buscar=request.GET.get('buscar',None)
    data=request.GET.get('data',None)  
   
    especialidade= get_object_or_404(Especialidade,id=id)
    

    if buscar:             
            pacientes_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').filter(\
                                                            especialidade__id=especialidade.id).filter(Q(paciente__nome_completo__icontains=buscar)|\
                                                            Q(paciente__cpf__icontains=buscar)).order_by('-created_at')
    if data:
            pacientes_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').filter(especialidade__id=especialidade.id).filter(data_pedido__iexact=data).order_by('-created_at')
        

    paginator = Paginator(pacientes_especialidade, 10)  
    page_number = request.GET.get("page")
    page_obj= paginator.get_page(page_number)
    
    context={
        'page_obj':page_obj,
        'especialidade':especialidade,
    }
    
    return render(request,template_name,context)

class PacienteEspecialidadeDetailView(DetailView):

    model=PacienteEspecialidade
    template_name='paciente_especialidade/detail_paciente_especialidade.html'
 
    
    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        paciente_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').get(id=self.kwargs['pk'])
        context['especialiadade']=paciente_especialidade.especialidade
        context['paciente_especialidade']=paciente_especialidade
       
        return context
        


