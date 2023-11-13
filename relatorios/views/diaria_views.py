
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render,redirect
from reportlab.lib.pagesizes import A4
from despesas.models import Diaria
from relatorios.forms import RelatorioForm
from datetime import datetime
def relatorio_diaria_pdf(request,context):
    
    response = HttpResponse(content_type='application/pdf')
    diarias=Diaria.objects.select_related('profissional').filter(data_diaria__gte=context['inicial']).filter(data_diaria__lte=context['final'])
  
    
    context['qta_diarias']=Diaria.objects.select_related('profissional').filter(data_diaria__gte=context['inicial']).filter(data_diaria__lte=context['final']).count()
    total=0 

    context['inicial']='{}/{}/{}'.format( context['inicial'][8:10],context['inicial'][5:7], context['inicial'][0:4])
    context['final']='{}/{}/{}'.format( context['final'][8:10],context['final'][5:7], context['final'][0:4])
    

    for d in diarias:
        total+=d.total
        
    context['total_diarias']=total

    html_string = render_to_string('diaria/relatorio_diaria_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def relatorio_diaria(request):
    
    response = HttpResponse(content_type='application/pdf')
    diarias=Diaria.objects.select_related('profissional').all()
    context={}
    if request.method == 'POST':
        form=RelatorioForm(request.POST or None)

        if form.is_valid():
          context['inicial']=form.cleaned_data.get('data_inicial')
          context['final']=form.cleaned_data.get('data_final')
      
          return relatorio_diaria_pdf(request,context)


    else:
        form=RelatorioForm(request.POST or None)    
        
  
    """   context={}
    if request.method == 'POST':
        erros={}
        data_inicial=request.POST.get('data_inicial',None)
        data_final=request.POST.get('data_final',None)
        print('233',data_inicial,data_final)

        if data_inicial > data_final:
            erros['data_inicial']='Data inicial maior que data final'
        
        if erros:
            context['erros']=erros  """

    return render(request,'diaria/relatorio_diaria.html',{'form':form})           
