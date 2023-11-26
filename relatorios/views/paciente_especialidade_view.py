
from django.shortcuts import render
from django.http import  HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import render
from relatorios.forms.paciente_especialidade_form import RelatorioPacienteEspecialidadeForm
from especialidades.models import PacienteEspecialidade
from django.db.models import Q
from datetime import datetime

def relatorio_paciente_especialidade_pdf(request,context):
    paciente_especialidade=PacienteEspecialidade.objects.select_related('paciente','especialidade','profissional').all()

    especialidade=context['especialidade']
    profissional=context['profissional']
    tipo_atendimento=context['tipo_atendimento'] 
    classificacao=context['classificacao']
    status=context['status']


    """  paciente_especialidade=paciente_especialidade.filter(Q(especialidade=especialidade)| Q(profissional=profissional)|\
                                                    Q(tipo_atendimento=tipo_atendimento) | Q(classificacao=classificacao) )
    print('paciente',paciente_especialidade)
    """  
    if especialidade:
        paciente_especialidade=paciente_especialidade.filter(especialidade=especialidade)   
    if profissional:
        paciente_especialidade=paciente_especialidade.filter(profissional=profissional) 
    if tipo_atendimento:
        paciente_especialidade=paciente_especialidade.filter(tipo_atendimento=tipo_atendimento)
    if classificacao:
        paciente_especialidade=paciente_especialidade.filter(classificacao=classificacao)
    if status:
        paciente_especialidade=paciente_especialidade.filter(status=status)


    context['qta_pacienteespecialidade']= paciente_especialidade.count()
    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['pacientes_especialidade']=paciente_especialidade

    
    response = HttpResponse(content_type='application/pdf')   
    html_string = render_to_string('paciente_especialidade/relatorio_paciente_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    
    return response

def relatorio_pacientes_especialidade(request):
    
    context={}
    if request.method == 'POST':
        form=RelatorioPacienteEspecialidadeForm(request.POST or None)

        if form.is_valid():
            context['especialidade']=form.cleaned_data.get('especialidades')
            context['profissional']=form.cleaned_data.get('profissionais')
            context['tipo_atendimento']=form.cleaned_data.get('tipo_atendimento')
            context['classificacao']=form.cleaned_data.get('classificacao')
            context['status']=form.cleaned_data.get('status')


            return relatorio_paciente_especialidade_pdf(request,context)

    else:
        form=RelatorioPacienteEspecialidadeForm(request.POST or None)

    return render(request,'paciente_especialidade/relatorio_paciente_especialidade.html',{'form':form})