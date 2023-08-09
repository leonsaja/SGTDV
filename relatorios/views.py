import io

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from despesas.models import Diaria


def relatorioDiaria(request):

    response = HttpResponse(content_type='application/pdf')

    data=[                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        ['teste','hoje','quinta','sexta', 'domingo','sabado','Segunda'],
        ['teste','hoje','quinta','sexta', 'domingo','sabado','Segunda'],
    ]
    fileName= 'pdftable.pdf' 
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate


    pdf = SimpleDocTemplate(fileName,pagesize=letter)

    from reportlab.platypus import Table
    table = Table(data)

    elems=[]
    elems.append(table)

    response=pdf.build(elems)
    return response


    """ 

    response= HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment;filename="mydata.pdf"'
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer,pagesize=A4)
    p.setTitle('ola mundo ')

    data=[
        ['id','profissional','descricao','data_diaria']
    ]
    for obj in Diaria.objects.all():
        data.append([obj.id, obj.profissional.nome_completo, obj.descricao, obj.data_diaria])

    # Draw the table
    x = 50
    y = 750
    for row in data:
        for item in row:
            p.drawString(x, y, str(item))
            x += column_width
        x = 50
        y -= row_height

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response

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
     buffer.seek(0)
    return HttpResponse(buffer, as_attachment=True, filename="hello.pdf")
    """
    """ response = HttpResponse(content_type='application/pdf')
    template=get_template('diarias/relatorio_diarias.html')
    context={'diarias': Diaria.objects.all()}
    html_string=template.render(context) """
    # Render the template with the data from the Django model
    """   html_string = render_to_string('diarias/relatorio_diarias.html', {'diarias': Diaria.objects.all()}) """

    # Create the PDF from the HTML string
    """ HTML(string=html_string).write_pdf(response)

    return response """