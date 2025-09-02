
from especialidades.models import AtendimentoEspecialidade, PacienteSia,PacienteEspecialidade
from especialidades.forms.form_atendimento_especialidade import AtendimentoEspecialidadeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.messages import constants
from django.contrib.messages.views import SuccessMessageMixin
from especialidades.forms.form_paciente_set import AtendPacienteSet
from rolepermissions.mixins import HasRoleMixin
from django.views.generic import DetailView, ListView,DeleteView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404 
from django.urls import reverse_lazy
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q


@has_role_decorator(['regulacao'])   
def atend_especialidade_create(request):
    atend_especialidade = AtendimentoEspecialidade()

    if request.method == 'POST':
        form = AtendimentoEspecialidadeForm(request.POST, instance=atend_especialidade, prefix='atendimento')
        formset = AtendPacienteSet(request.POST, instance=atend_especialidade, prefix='paciente')

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.add_message(request, constants.SUCCESS, 'Atendimento salvo com sucesso!')
            return redirect('especialidades:list-atend_especialidade')
        else:
            # SE O FORMSET TIVER ERROS, ENVIAMOS A MENSAGEM
            # O erro de 'unique_together' fica em 'non_form_errors' ou 'non_field_errors'
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.add_message(request, constants.ERROR, f'Paciente duplicado: {error}')

            # Também é bom verificar os erros de cada formulário individual
           
    else:
        form = AtendimentoEspecialidadeForm(instance=atend_especialidade, prefix='atendimento')
        formset = AtendPacienteSet(instance=atend_especialidade, prefix='paciente')

    return render(request, 'atendimento_especialidade/form_atend_especialidade.html', {'form': form, 'formset': formset})

@has_role_decorator(['regulacao'])  
def atend_especialidade_update(request,id):
    
    atend_especialidade=get_object_or_404(AtendimentoEspecialidade,pk=id)
   
    if request.method == 'POST':

        form = AtendimentoEspecialidadeForm(request.POST,instance=atend_especialidade,prefix='atendimento' )
        formset=AtendPacienteSet(request.POST,instance=atend_especialidade,prefix='paciente')
        if form.is_valid() and formset.is_valid():
            
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Atendimento salvo com sucesso')
            return redirect('especialidades:list-atend_especialidade')
        
        else:
            # SE O FORMSET TIVER ERROS, ENVIAMOS A MENSAGEM
            # O erro de 'unique_together' fica em 'non_form_errors' ou 'non_field_errors'
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.add_message(request, constants.ERROR, f'Paciente duplicado: {error}')


    else:
        form = AtendimentoEspecialidadeForm(request.POST or None,instance=atend_especialidade,prefix='atendimento')
        formset=AtendPacienteSet(request.POST or None,instance=atend_especialidade,prefix='paciente')
    
    return render(request, 'atendimento_especialidade/form_atend_especialidade.html', {'form': form,'formset':formset})

class AtendEspecialidadeListView(HasRoleMixin,ListView):


    model=AtendimentoEspecialidade
    template_name='atendimento_especialidade/list_atend_especialidade.html'
    context_object_name='atend_especialidades'
    paginate_by=10
    allowed_roles=['regulacao','secretario','coordenador','recepcao']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related('especialidade')

        buscar=self.request.GET.get('buscar',None)
        status=self.request.GET.get('status',None)
        data = self.request.GET.get('data', None)

        if buscar:
            queryset=qs.filter(especialidade__nome__icontains=buscar)
    
        if status:
            queryset=qs.filter(status=status)

        if data:
            queryset = qs.filter(data__iexact=data)

        if not buscar and not status and not data:
                queryset=qs.exclude(status='2')
        return queryset.order_by('-especialidade')
    
class AtendEspecialidadeDetailView(HasRoleMixin,DetailView):


    model=AtendimentoEspecialidade
    template_name='atendimento_especialidade/detail_atend_especialidade.html'
    allowed_roles=['regulacao','recepcao','secretario','coordenador']
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        atendimento_especialidade= AtendimentoEspecialidade.objects.select_related('especialidade').get(id=self.kwargs['pk'])
        
        context['atendimento_especialidade']=atendimento_especialidade
        context['pacientes_set']=PacienteSia.objects.select_related('paciente').filter(atendimento_paciente__id=atendimento_especialidade.id)
        return context
    
class AtendEspecialidadeDeleteView(HasRoleMixin,SuccessMessageMixin, DeleteView):


    model=AtendimentoEspecialidade
    success_url=reverse_lazy('especialidades:list-atend_especialidade')
    success_message='Registro excluido com sucesso '
    allowed_roles=['coordenador']


    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)
    
@has_role_decorator(['regulacao','coordenador','recepcao','secretario'])  
def atend_especialidade_pdf(request,id):
    atendimento_especialidade=get_object_or_404(AtendimentoEspecialidade,id=id)
    context={}

    context['atendimento_especialidade']= AtendimentoEspecialidade.objects.select_related('especialidade').get(id=atendimento_especialidade.id)
    context['pacientes_set']=PacienteSia.objects.select_related('paciente').filter(atendimento_paciente__id=context['atendimento_especialidade'].id)
   
                
    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('atendimento_especialidade/pdf_atend_especialidade.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)


    return response

@login_required
def load_pacientes_by_especialidade(request):
    especialidade_id = request.GET.get('especialidade_id')
    pacientes_data = []

    if especialidade_id:
        try:
            
            pacientes_especialidade = PacienteEspecialidade.objects.select_related('paciente','especialidade','procedimento').filter(Q(status='1')|Q(status='4'),especialidade_id=especialidade_id).order_by('paciente__nome_completo')
            
            for pe in pacientes_especialidade:
                
                pacientes_data.append({
                    'id': pe.id,
                    'nome_completo': pe.paciente.nome_completo,
                    'cns':pe.paciente.cns,
                    'dt_nascimento':pe.paciente.dt_nascimento.strftime('%d/%m/%Y'),
                    'procedimento': pe.procedimento.nome_procedimento, # Formata a data para exibir
                    'classificacao':pe.get_classificacao_display(),
                   
                })
                
        except ValueError:
            pass 
        except Exception as e:
            print(f"Erro ao carregar pacientes: {e}")
            pass

    return JsonResponse(pacientes_data, safe=False)

