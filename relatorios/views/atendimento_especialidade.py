from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from especialidades.models import AtendimentoEspecialidade
from relatorios.forms.atendimento_especialidade_form import RelatorioAtendimentoEspecialidadeForm
from weasyprint import HTML



def relatorio_atendimento_pdf(request,context):
    response = HttpResponse(content_type='application/pdf')
    atendimentos=AtendimentoEspecialidade.objects.select_related('especialidade').all()
    print('atendimentos',atendimentos)
    especialidade= context['especialidade']
    data_inicial=context['inicial']
    data_final=context['final']
    atendimento_via=context['atendimento_via']
    
    print('10',atendimento_via)
    
    if especialidade:                                                                                                                                                                                                                                                   
        atendimentos=atendimentos.filter(especialidade=especialidade) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if data_inicial and data_final:
        atendimentos=atendimentos.filter(data__gte=data_inicial).filter(data__lte=data_final)

    if atendimento_via:
        atendimentos=atendimentos.filter(atendimento_via=atendimento_via)
    context['qta_atendimeento']= atendimentos.count()
    total=0

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['atendimentos']=atendimentos

    
    for a in atendimentos:
       print('atendimento',a)
       total=a.atend_paciente_especialidade.count()    
    context['total']=total
    
    html_string = render_to_string('especialidade/relatorio_atendimento_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def relatorio_atendimento_especialidade(request):
    context={}
    

    if request.method == 'POST':
        form=RelatorioAtendimentoEspecialidadeForm(request.POST or None)
        
        if form.is_valid():
          context['inicial']=form.cleaned_data.get('data_inicial')
          context['final']=form.cleaned_data.get('data_final')
          context['especialidade']=form.cleaned_data.get('especialidade')
          context['atendimento_via']=form.cleaned_data.get('atendimento_via')
          return relatorio_atendimento_pdf(request,context)
         

    else:
        form=RelatorioAtendimentoEspecialidadeForm(request.POST or None)    
        
    return render(request,'especialidade/atendimento_especialidade.html',{'form':form})           
