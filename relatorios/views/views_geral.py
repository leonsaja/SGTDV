import io

from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.shortcuts import get_object_or_404, render
from relatorios.forms import RelatorioForm
from django.views import View
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from relatorios.forms import RelatorioForm
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
    """  response = HttpResponse(content_type='application/pdf')
   

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,pagesize=A4)

    # Define the width and height of each row in the table
    row_height = 20
    column_width = 50

    # Define the data to be printed in the table
    
    
    p.drawString(260, 800, "Hello world.")

    data=  [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
    t=Table(data)
    t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
                            ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
    
    elems=[]
    elems.append(t)
    response.
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
 

    #adicionar um sub title
    p.setFont('Helvetica-Bold',13)
    p.setFillColor(colors.red)
    p.drawCentredString(300,740,'HOJE NOVO DIA')



    #Adicionar uma linha Horizontal
    p.setStrokeColor(colors.blue)
    p.setLineWidth(5)
    p.line(30,730,550,730)
  
   

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    
    buffer.seek(0)
    return HttpResponse(buffer, as_attachment=True, filename="hello.pdf")
    
    
    response = HttpResponse(content_type='application/pdf')


    template=get_template('diarias/relatorio_diarias.html')
    context={'diarias': Diaria.objects.all()}
    html_string=template.render(context)
    # Render the template with the data from the Django model
    
    html_string = render_to_string('diarias/relatorio_diarias.html', {'diarias': Diaria.objects.all()}) 

    # Create the PDF from the HTML string
    HTML(string=html_string).write_pdf(response)

    return respons 

    """

def relatorio_diaria_pdf(request,teste):
    response = HttpResponse(content_type='application/pdf')
    diarias=Diaria.objects.select_related('profissional').all()
    context={}
    context['qta_diarias']=Diaria.objects.select_related('profissional').count()
    total=0 
    for d in diarias:
        total+=d.total
    context['total_diarias']=total

    html_string = render_to_string('diaria/relatorio_diaria_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
    
    

    """ response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('diarias/relatorio_diaria_pdf.html',{'diaria':diaria})
    
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

   
    return response """

def relatorioReembolsoPdf(request,id):

    diaria=get_object_or_404(Diaria,id=id)
    context={}
    context['diaria']=diaria
    context['reembolsos'] =Reembolso.objects.select_related('diaria').filter(diaria__id=diaria.id)
    response = HttpResponse(content_type='application/pdf')
    context['movimentacao']=context['reembolsos'][0].movimentacao
    html_string = render_to_string('reembolsos/relatorio_reembolso_pdf.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

   
    return response

def relatorioReciboTfdPdf(request,id):
    recibo_pdf=get_object_or_404(ReciboTFD,id=id)
    context={}

    context['recibo_tfd']= ReciboTFD.objects.select_related('paciente','acompanhante').get(id=recibo_pdf.id)
    context['recibo_codigo']=CodigoSIA.objects.select_related('recibo_tfd').filter(recibo_tfd__id=context['recibo_tfd'].id)
    
    
    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('tfds/recibo_tfds/relatorio_recibo_tfd_pdf.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)


    return response