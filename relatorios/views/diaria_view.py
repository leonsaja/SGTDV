
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render,redirect
from reportlab.lib.pagesizes import A4
from despesas.models import Diaria
from relatorios.forms.diaria_form import RelatorioDiariaForm
from datetime import datetime
from rolepermissions.decorators import has_role_decorator

def relatorio_diaria_pdf(request,context):
    response = HttpResponse(content_type='application/pdf')
    
    if context['profissional']:
        diarias=Diaria.objects.select_related('profissional').filter(profissional=context['profissional']).filter(data_diaria__gte=context['inicial']).filter(data_diaria__lte=context['final'])
  
    else:
        diarias=Diaria.objects.select_related('profissional').filter(data_diaria__gte=context['inicial']).filter(data_diaria__lte=context['final'])

    context['qta_diarias']= diarias.count()
    context['qta_reembolsos']=diarias.filter(reembolso='1').count()
        
    total=0
    total_reembolsos=0
   

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    

    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['diarias']=diarias

  
    for d in diarias:
        total+=d.total

        for r in d.reembolsos.all():
            if r.valor_desp:
                total_reembolsos+=r.valor_desp
    

    
    context['total_diarias']=total
    context['total_reembolsos']=total_reembolsos
    

    html_string = render_to_string('diaria/relatorio_diaria_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

@has_role_decorator(['secretario','digitador','coordenador'])
def relatorio_diaria(request):
    context={}
    diarias=Diaria.objects.select_related('profissional').order_by('-created_at')

    if request.method == 'POST':
        form=RelatorioDiariaForm(request.POST or None)


        print('data_final',request.GET.get('data_final'))

        if form.is_valid():
          context['inicial']=form.cleaned_data.get('data_inicial')
          context['final']=form.cleaned_data.get('data_final')
          context['profissional']=form.cleaned_data.get('profissionais')
      
          return relatorio_diaria_pdf(request,context)

    else:
        form=RelatorioDiariaForm(request.POST or None)    
        
    return render(request,'diaria/relatorio_diaria.html',{'form':form,'diarias':diarias})           
