from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from weasyprint import HTML
from django.db.models import Q

from django.shortcuts import get_object_or_404, render,redirect
from reportlab.lib.pagesizes import A4
from cidadao.models import Cidadao
from datetime import datetime
from rolepermissions.decorators import has_role_decorator


@has_role_decorator(['coordenador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))

def relatorio_cadastro_cidadao(request):
    context={}
    response = HttpResponse(content_type='application/pdf')   
    cidadaos=Cidadao.objects.select_related('microarea').filter(Q(cns=None)|Q(cpf=None))
    context['cadastros']= cidadaos
    context['data']=datetime.today().strftime('%d/%m/%Y') 


    html_string = render_to_string('cidadao/relatorio_cidadao_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
        
        
