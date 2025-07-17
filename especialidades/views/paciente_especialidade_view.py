
from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from especialidades.forms.form_paciente_especialidade import PacienteEspecialidadeForm,PacienteEspecialidadeUpdateForm
from especialidades.models import Especialidade, PacienteEspecialidade
from django.contrib import messages
from django.contrib.messages import constants
from django.views.generic import DetailView, CreateView,UpdateView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin


class PacienteEspecialidadeCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
    model = PacienteEspecialidade
    form_class = PacienteEspecialidadeForm
    template_name = 'paciente_especialidade/form_paciente_especialidade.html'
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['recepcao','regulacao']
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialidade'] = get_object_or_404(Especialidade, id=self.kwargs.get('id'))
        return context
  
    def form_valid(self, form):
        form.instance.especialidade = get_object_or_404(Especialidade, id=self.kwargs.get('id'))
        return super().form_valid(form)
    
    def get_success_url(self):
        especialidade_id = self.object.especialidade.id
        return reverse_lazy('especialidades:detail-especialidade', kwargs={'pk': especialidade_id})
    
class PacienteEspecialidadeUpdateView(HasRoleMixin,UpdateView):
    model = PacienteEspecialidade
    form_class = PacienteEspecialidadeUpdateForm
    template_name = 'paciente_especialidade/form_paciente_especialidade.html'
    pk_url_kwarg = 'id' 
    allowed_roles=['recepcao','regulacao']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especialidade'] = self.object.especialidade
        return context
    
    def form_valid(self, form):  
        messages.add_message(self.request, constants.SUCCESS, 'Dados atualizados com sucesso')
        return super().form_valid(form)

    def get_success_url(self):
        especialidade_id = self.object.especialidade.id
        return reverse_lazy('especialidades:detail-especialidade', kwargs={'pk': especialidade_id})

class PacienteEspecialidadeListView(HasRoleMixin,ListView):
   
    model = PacienteEspecialidade
    template_name = 'especialidade/detail_especialidade.html'
    paginate_by = 10
    pk_url_kwarg = 'id'
    allowed_roles=['recepcao','regulacao','secretario','coordenador','acs']

    def get_queryset(self):
        especialidade_id = self.kwargs.get(self.pk_url_kwarg)

        buscar = self.request.GET.get('buscar', None)
        data = self.request.GET.get('data', None)

        queryset = PacienteEspecialidade.objects.select_related(
            'paciente', 'especialidade', 'procedimento'
        ).filter(especialidade__id=especialidade_id).order_by('-created_at')

        if buscar:
            queryset = queryset.filter(
                Q(paciente__nome_completo__icontains=buscar) | Q(paciente__cpf__icontains=buscar)
            )

        if data:
            queryset = queryset.filter(data_pedido__iexact=data)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        especialidade_id = self.kwargs.get(self.pk_url_kwarg)
        context['especialidade'] = get_object_or_404(Especialidade, id=especialidade_id)
        return context

class PacienteEspecialidadeDetailView(HasRoleMixin,DetailView):

    model=PacienteEspecialidade
    template_name='paciente_especialidade/detail_paciente_especialidade.html'
    allowed_roles=['recepcao','secretario','regulacao','coordenador','acs']
    
    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        paciente_especialidade=PacienteEspecialidade.objects.select_related('paciente','procedimento','especialidade').get(id=self.kwargs['pk'])
        context['especialiadade']=paciente_especialidade.especialidade
        context['paciente_especialidade']=paciente_especialidade
       
        return context
        
@has_role_decorator(['secretario','coordenador'])
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

