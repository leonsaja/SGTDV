from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render,redirect
from reportlab.lib.pagesizes import A4
from especialidades.models import Especialidade
from relatorios.forms.especialidade_form import RelatorioEspecialidadeForm
from datetime import datetime

def relatorio_especialidade_pdf(request,context):
    pass
   

def relatorio_especialidade(request):
    context={}
    response = HttpResponse(content_type='application/pdf')   
    especialidades=Especialidade.objects.all().order_by('nome')

    context['qta_especialidade']= especialidades.count()
    context['especialidades']=especialidades
    context['data']=datetime.today().strftime('%d/%m/%Y') 


    html_string = render_to_string('especialidade/relatorio_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
        
        
