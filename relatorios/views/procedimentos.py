from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from especialidades.models import ProcedimentosEspecialidade
from datetime import datetime
from rolepermissions.decorators import has_role_decorator


has_role_decorator(['coordenador'],redirect_url='usuarios:acesso_negado')

def relatorio_procedimentos(request):
    context={}
    response = HttpResponse(content_type='application/pdf')   
    procedimentos=ProcedimentosEspecialidade.objects.all().order_by('nome_procedimento')
    context['procedimentos']= procedimentos
    context['data']=datetime.today().strftime('%d/%m/%Y') 


    html_string = render_to_string('procedimento/relatorio_procedimentos_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
        
        
