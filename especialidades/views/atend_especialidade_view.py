
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
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q
from dal import autocomplete
from io import BytesIO



@has_role_decorator(['regulacao'])   
def atend_especialidade_create(request):
    atend_especialidade = AtendimentoEspecialidade()

    if request.method == 'POST':
        form = AtendimentoEspecialidadeForm(request.POST, instance=atend_especialidade, prefix='atendimento')
        formset = AtendPacienteSet(request.POST, instance=atend_especialidade, prefix='paciente')

        if form.is_valid() and formset.is_valid():
            atendimento=form.save(commit=False)
            atendimento.criado_por=request.user.nome_completo
            atendimento.save()
            formset.save()
            messages.add_message(request, constants.SUCCESS, 'Atendimento salvo com sucesso!')
            return redirect('especialidades:list-atend_especialidade')
        else:
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.add_message(request, constants.ERROR, f'Paciente duplicado: {error}')       
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
            
            atendimento=form.save(commit=False)
            atendimento.alterado_por=request.user.nome_completo
            atendimento.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Atendimento salvo com sucesso')
            return redirect('especialidades:list-atend_especialidade')
        
        else:
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

        buscar=self.request.GET.get('buscar',None).rstrip()
        status=self.request.GET.get('status',None)
        data = self.request.GET.get('data', None)

        if buscar:
            qs=qs.filter(especialidade__nome__icontains=buscar)
    
        if status:
            qs=qs.filter(status=status)

        if data:
            qs = qs.filter(data__iexact=data)

        if not buscar and not status and not data:
                qs=qs.filter(status='1')
        return qs.order_by('-data')
    
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
def atend_especialidade_pdf(request, id):
    atendimento_especialidade = get_object_or_404(
        AtendimentoEspecialidade.objects.select_related('especialidade'),
        id=id
    )

    # 2. Busca a lista de pacientes relacionada, também otimizando.
    lista_pacientes = PacienteSia.objects.select_related('paciente').filter(
        atendimento_paciente=atendimento_especialidade
    ).order_by('paciente__paciente__nome_completo')

    context = {
        'atendimento_especialidade': atendimento_especialidade,
        'pacientes_set': lista_pacientes,
    }

    # 3. Renderiza o template HTML.
    html_string = render_to_string(
        'atendimento_especialidade/pdf_atend_especialidade.html',
        context
    )

    # 4. Cria um buffer na memória para o PDF.
    buffer = BytesIO()

    # 5. Gera o PDF usando WeasyPrint e salva no buffer.
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    
    # 6. Prepara a resposta HTTP para download.
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="atendimento_{id}.pdf"'
    
    return response


class PacienteAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        
        if not self.request.user.is_authenticated:
            return PacienteEspecialidade.objects.none()

        especialidade_id = self.forwarded.get('atendimento-especialidade', None)        
    
        if especialidade_id:
            qs = PacienteEspecialidade.objects.select_related('paciente','especialidade','procedimento').filter(Q(status='1')|Q(status='4')|Q(status='5'),especialidade__id=especialidade_id).order_by('paciente__nome_completo')
        else:
            return PacienteEspecialidade.objects.none()

        if self.q:
            self.q=self.q.rstrip()
            qs = qs.filter(
                Q(paciente__nome_completo__unaccent__icontains=self.q) |
                Q(paciente__cns__icontains=self.q)
            ).filter(Q(status='1')|Q(status='5'))

        return qs
