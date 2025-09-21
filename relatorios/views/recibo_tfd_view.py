from django.shortcuts import render
from relatorios.forms.recibo_tfd_form import RelatorioReciboTfdsForm
from tfds.models import ReciboTFD
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from django.core.paginator import Paginator
from io import BytesIO
from datetime import date
from rolepermissions.decorators import has_role_decorator

def relatorio_recibo_tfd_pdf(request,context):
    recibo_tfds=ReciboTFD.objects.select_related('paciente').filter(data__gte=context['inicial']).filter(data__lte=context['final']).order_by('paciente__nome_completo')
  
    if context['paciente']:
        recibo_tfds=recibo_tfds.filter(paciente=context['paciente'])

    
    if context['especialidade']:
        recibo_tfds=recibo_tfds.filter(especialidade=context['especialidade']).distinct('paciente__cpf').order_by('paciente__cpf','paciente__nome_completo')

    if context['fora_estado']:
        recibo_tfds=recibo_tfds.filter(atend_fora_estado=context['fora_estado'])

   
    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['data']=datetime.today().strftime('%d/%m/%Y')

    total=0
    for r in recibo_tfds:
            total+=r.total_pag()
    

    context['qta_recibo_tfds']= recibo_tfds.count()
    context['recibos_tfds']=recibo_tfds
    context['total_recibo']=total



    buffer = BytesIO()
    html_string = render_to_string('tfds/recibo_tfd/relatorio_recibo_tfd_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Relatorio_Recibo_TFDs_{date.today().strftime("%d/%m/%Y")}.pdf"'
    return response

@has_role_decorator(['coordenador','secretario','regulacao'])
def relatorio_recibo_tfd(request):
    context={}
    
    recibos_tfds=ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').all().order_by('-created_at')
    paginator = Paginator(recibos_tfds,9)  
    page_number = request.GET.get("page")
  
    recibos_tfds= paginator.get_page(page_number)
  
    if request.method == 'POST':
        form=RelatorioReciboTfdsForm(request.POST or None)
        
        if form.is_valid():
            context['inicial']=form.cleaned_data.get('data_inicial')
            context['final']=form.cleaned_data.get('data_final')
            context['paciente']=form.cleaned_data.get('pacientes')
            context['especialidade']=form.cleaned_data.get('especialidade')
            context['fora_estado']=form.cleaned_data.get('fora_estado')
            context['tipo_relatorio']=form.cleaned_data.get('tipo_relatorio')

            return relatorio_recibo_tfd_pdf(request,context)
           
    else:
        form=RelatorioReciboTfdsForm(request.POST or None)

    return render(request,'tfds/recibo_tfd/relatorio_recibo_tfd.html',{'form':form,'recibos_tfds':recibos_tfds})