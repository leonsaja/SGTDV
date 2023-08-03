import io
from django.shortcuts import render
from django.views import View

from django.views.generic import ListView
from despesas.models import Diaria
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
def relatorioDiaria(request):
    response= HttpResponse(content_type='application/pdf')
    
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer,pagesize=A4)
    p.setTitle('ola mundo ')
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(260, 800, "Hello world.")
   
 

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
    """ buffer.seek(0)
    return HttpResponse(buffer, as_attachment=True, filename="hello.pdf")
    """
    
