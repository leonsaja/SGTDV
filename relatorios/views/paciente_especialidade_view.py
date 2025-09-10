
from django.shortcuts import render
from django.http import  HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import render
from relatorios.forms.paciente_especialidade_form import RelatorioPacienteEspecialidadeForm
from especialidades.models import PacienteEspecialidade
from django.db.models import Q
from datetime import datetime
from rolepermissions.decorators import has_role_decorator


def relatorio_paciente_especialidade_pdf(request,context):
    paciente_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','procedimento').order_by('paciente__nome_completo')

    especialidade=context['especialidade']
    profissional=context['profissional']
    procedimento=context['procedimento']
    classificacao=context['classificacao']
    status=context['status']

    if especialidade:
        paciente_especialidade=paciente_especialidade.filter(especialidade=especialidade)   
    if profissional:
        paciente_especialidade=paciente_especialidade.filter(profissional=profissional) 
    if procedimento:
        paciente_especialidade=paciente_especialidade.filter(procedimento=procedimento)
    if classificacao:
        paciente_especialidade=paciente_especialidade.filter(classificacao=classificacao)
    if status:
        paciente_especialidade=paciente_especialidade.filter(status=status)


    context['qta_pacienteespecialidade']= paciente_especialidade.count()
    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['pacientes_especialidade']=paciente_especialidade

    if context['procedimento']:
        
        if context['procedimento'].nome_procedimento=='EXAMES':
            context['exames']=context['procedimento']
    
    response = HttpResponse(content_type='application/pdf')   
    html_string = render_to_string('paciente_especialidade/relatorio_paciente_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    
    return response

has_role_decorator(['regulacao','coordenador','secretario'])
def relatorio_pacientes_especialidade(request):
    
    context={}
    if request.method == 'POST':
        form=RelatorioPacienteEspecialidadeForm(request.POST or None)

        if form.is_valid():
            context['especialidade']=form.cleaned_data.get('especialidades')
            context['profissional']=form.cleaned_data.get('profissionais')
            context['procedimento']=form.cleaned_data.get('procedimento')
            context['classificacao']=form.cleaned_data.get('classificacao')
            context['status']=form.cleaned_data.get('status')


            return relatorio_paciente_especialidade_pdf(request,context)

    else:
        form=RelatorioPacienteEspecialidadeForm(request.POST or None)

    return render(request,'paciente_especialidade/relatorio_paciente_especialidade.html',{'form':form})