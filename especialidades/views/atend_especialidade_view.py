from django.shortcuts import get_object_or_404, render
from especialidades.models import PacienteEspecialidade,Especialidade,AtendimentoEspecialidade
from especialidades.forms.form_AtendimentoEspecialidade import AtendPacienteformset,AtendEspecialidadeForm
from django.views.generic import ListView
from django.http import HttpResponse

def atenEspecialidadeCreate(request,id):

    especialidade= get_object_or_404(Especialidade,id=id)

    atend=AtendimentoEspecialidade()
   
    
    if request.method=='POST':
        
        form=AtendEspecialidadeForm(request.POST)    
        atendformset=AtendPacienteformset(request.POST,instance=atend,prefix='paciente')
        
        if form.is_valid() and  atendformset.is_valid():
            form=form.save(commit=False)
            form.save()
            atendformset.save()
            return HttpResponse('OPERACAO REALIZADO COM SUCESSO ')  
    
    form=AtendEspecialidadeForm(request.POST or None)
    atendformset=AtendPacienteformset(request.POST or None,instance=atend,prefix='paciente')
    return render(request,'atend_especialidades/form_atend_especialidade.html',{'form':form,'formset':atendformset,'especialidade':especialidade})


class EspecialidadeListView(ListView):
    model=PacienteEspecialidade
    template_name='atend_especialidades/form_atend_especialidade.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    



