from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from especialidades.models import AtendimentoEspecialidade, PacienteSia
from relatorios.forms.atendimento_especialidade_form import RelatorioAtendimentoEspecialidadeForm
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from io import BytesIO
from datetime import date


@login_required
def relatorio_atendimento_pdf(request,context):

    especialidade= context['especialidade']
    data_inicial=context['inicial']
    data_final=context['final']
    atendimento_via=context['atendimento_via']
    status=context['status']
    tipo=context['tipo']
    qta_pacientes=0
    atendimentos=AtendimentoEspecialidade.objects.select_related('especialidade').filter(data__gte=data_inicial).filter(data__lte=data_final)
    
        
    if tipo == '2': 
        atendimentos=AtendimentoEspecialidade.objects.select_related('especialidade').filter(data__gte=data_inicial).filter(data__lte=data_final).filter(especialidade=especialidade).filter(status=status)
        
        queryset = PacienteSia.objects.select_related(
            'atendimento_paciente', 
            'paciente__paciente',
            'atendimento_paciente__especialidade'
        ).all()

        
        if especialidade:
            queryset = queryset.filter(atendimento_paciente__especialidade=especialidade)
            
        if data_inicial and data_final:
            # Usando __range, o campo 'data' está no modelo AtendimentoEspecialidade
            queryset = queryset.filter(atendimento_paciente__data__range=[data_inicial, data_final])
          
        # Filtro de Via de Atendimento (acessado via 'atendimento_paciente')
        if atendimento_via:
            queryset = queryset.filter(atendimento_paciente__atendimento_via=atendimento_via)

        # Filtro de Status do Atendimento (acessado via 'atendimento_paciente')
        if status:
            queryset = queryset.filter(atendimento_paciente__status=status)
        
        qta_pacientes=queryset.count()
        dados_relatorio = queryset
    
    else:
        if especialidade:                                                                                                                                                                                                                                                   
            atendimentos=atendimentos.filter(especialidade=especialidade) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        if atendimento_via:
            atendimentos=atendimentos.filter(atendimento_via=atendimento_via)

        if status:
            atendimentos=atendimentos.filter(status=status)
            
        dados_relatorio=atendimentos
        
    
    context['qta_atendimento']= atendimentos.count()
    context['qta_pacientes']=qta_pacientes
    
    total=0

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['atendimentos']=dados_relatorio

    
    for a in atendimentos:
       total+=a.qta_paciente_especialidade_concluido() 
    context['total']=total

    data=date
    buffer = BytesIO()
    html_string = render_to_string('especialidade/relatorio_atendimento_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Relatorio_Atendimento_{date.today().strftime("%d/%m/%Y")}.pdf"'

    return response

@login_required
@has_role_decorator(['regulacao','coordenador','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def relatorio_atendimento_especialidade(request):
    context={}
    

    if request.method == 'POST':
        form=RelatorioAtendimentoEspecialidadeForm(request.POST or None)
        
        if form.is_valid():
          context['inicial']=form.cleaned_data.get('data_inicial')
          context['final']=form.cleaned_data.get('data_final')
          context['especialidade']=form.cleaned_data.get('especialidade')
          context['atendimento_via']=form.cleaned_data.get('atendimento_via')
          context['status']=form.cleaned_data.get('status')
          context['tipo']=form.cleaned_data.get('tipo')
          return relatorio_atendimento_pdf(request,context)
         

    else:
        form=RelatorioAtendimentoEspecialidadeForm(request.POST or None)    
        
    return render(request,'especialidade/atendimento_especialidade.html',{'form':form})           
