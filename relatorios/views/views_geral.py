import io

from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.shortcuts import get_object_or_404, render
from relatorios.forms.diaria_form import RelatorioDiariaForm
from django.views import View
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from relatorios.forms.diaria_form import RelatorioDiariaForm
from despesas.models import Diaria, Reembolso
from tfds.models import CodigoSIA, ReciboPassagemTFD, ReciboTFD


def relatorioDiaria(request):  
    response = HttpResponse(content_type='application/pdf')
    """ response['Content-Disposition'] = 'attachment; filename="mydata.pdf"' """

    # Render the template with the data from the Django model
    context={}
    context['diarias']=Diaria.objects.select_related('profissional').all()
    context['qta_diarias']=Diaria.objects.select_related('profissional').count()
    diarias=context['diarias']
    total=0 
   
    for d in diarias:
       total+=(d.total)

    context['total_diarias']=total

    html_string = render_to_string('diarias/relatorio_diarias.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
   