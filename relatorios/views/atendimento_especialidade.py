from datetime import datetime
from django.shortcuts import render

from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string

from especialidades.models import AtendimentoEspecialidade
from relatorios.forms.atendimento_especialidade_form import RelatorioAtendimentoEspecialidadeForm



def relatorio_atendimento_pdf(request,context):
    response = HttpResponse(content_type='application/pdf')
    
    if context['especialidade']:
        atendimentos=AtendimentoEspecialidade.objects.select_related('especialidade').filter(especialidade=context['especialidade']).filter(data__gte=context['inicial']).filter(data__lte=context['final'])
  
    else:
        atendimentos=AtendimentoEspecialidade.objects.select_related('especialidade').filter(data__gte=context['inicial']).filter(data__lte=context['final'])

    context['qta_atendimeento']= atendimentos.count()
  
        
    total=0
    total_reembolsos=0
   

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    from weasyprint import HTML

    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['atendimentos']=atendimentos

  
    for a in atendimentos:
       total=a.atend_paciente_especialidade.count()

    print(total)

    
    context['total']=total
    context['total_reembolsos']=total_reembolsos
    

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
      
          return relatorio_atendimento_pdf(request,context)
         

    else:
        form=RelatorioAtendimentoEspecialidadeForm(request.POST or None)    
        
    return render(request,'especialidade/atendimento_especialidade.html',{'form':form})           
