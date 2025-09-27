from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render,redirect
from reportlab.lib.pagesizes import A4
from especialidades.models import Especialidade
from relatorios.forms.especialidade_form import RelatorioEspecialidadeForm
from datetime import datetime
from rolepermissions.decorators import has_role_decorator
from io import BytesIO
from datetime import date


@has_role_decorator(['regulacao','coordenador','secretario'],redirect_url='usuarios:acesso_negado')

def relatorio_especialidade(request):
    context={}
    especialidades=Especialidade.objects.all().order_by('nome')

    context['qta_especialidade']= especialidades.count()
    context['especialidades']=especialidades
    context['data']=datetime.today().strftime('%d/%m/%Y') 

    buffer = BytesIO()
    html_string = render_to_string('especialidade/relatorio_especialidade_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Relatorio_Especialidade_{date.today().strftime("%d/%m/%Y")}.pdf"'

    return response
        
        
