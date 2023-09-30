from django.shortcuts import render
from especialidades.models import PacienteEspecialidade,Especialidade
from especialidades.forms.form_AtendimentoEspecialidade import Atendformset,AtendEspecialidadeForm
from django.views.generic import ListView
from django.http import HttpResponse

def atenEspecialidadeCreate(request):

    form=AtendEspecialidadeForm()
    atenEspformset=Atendformset()
    especialidades =Especialidade.objects.all()


    if request.method=='POST':
        form=AtendEspecialidadeForm(request.POST or None)
        atenEspformset=Atendformset(request.POST or None)
        print('form',form)
        print('aten',atenEspformset)
        if form.is_valid() and atenEspformset.is_valid():
            form=form.save()
            atenEspformset.save()
            return HttpResponse('OPERACAO REALIZADO COM SUCESSO ')  
        
    form=AtendEspecialidadeForm(request.POST or None)
    atenEspformset=Atendformset(request.POST or None)        
    return render(request,'atend_especialidades/form_atend_especialidade.html',{'form':form,'atenEspformset':atenEspformset,'especialidades':especialidades})


class EspecialidadeListView(ListView):
    model=PacienteEspecialidade
    template_name='atend_especialidades/form_atend_especialidade.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    



