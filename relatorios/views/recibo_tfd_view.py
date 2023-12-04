from django.shortcuts import render
from relatorios.forms.recibo_tfd_form import RelatorioReciboTfdsForm
from tfds.models import ReciboTFD
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from django.db import connection

def relatorio_recibo_tfd_pdf(request,context):
    recibo_tfds=ReciboTFD.objects.select_related('paciente').prefetch_related('procedimento_recibo_tfd').all()

    if context['inicial'] and context['final']:
        recibo_tfds=recibo_tfds.filter(data__gte=context['inicial']).filter(data__lte=context['final'])

    if context['paciente']:
        recibo_tfds=recibo_tfds.filter(paciente=context['paciente'])

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['data']=datetime.today().strftime('%d/%m/%Y')

    total=0
    for r in recibo_tfds:
            total+=r.total_pag()
    

    context['qta_recibo_tfds']= recibo_tfds.count()
    context['recibos_tfds']=recibo_tfds
    context['total_recibo']=total

    """  context['total_diarias']=total
    context['total_reembolsos']=total_reembolsos """
 

    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('tfds/recibo_tfd/relatorio_recibo_tfd_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

def relatorio_recibo_tfd(request):
    context={}
    
    
    if request.method == 'POST':
        form=RelatorioReciboTfdsForm(request.POST or None)

        if form.is_valid():
            context['inicial']=form.cleaned_data.get('data_inicial')
            context['final']=form.cleaned_data.get('data_final')
            context['paciente']=form.cleaned_data.get('pacientes')

            return relatorio_recibo_tfd_pdf(request,context)
           
    else:
        form=RelatorioReciboTfdsForm(request.POST or None)

    return render(request,'tfds/recibo_tfd/relatorio_recibo_tfd.html',{'form':form})