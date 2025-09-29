from django.shortcuts import render
from django.urls import reverse_lazy
from relatorios.forms.recibo_passagem_form import RelatorioReciboPassagemForm
from tfds.models import ReciboPassagemTFD
from django.http import  HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator


def relatorio_recibo_passagem_pdf(request,context):
    recibo_passagem=ReciboPassagemTFD.objects.select_related('paciente').all()

    if context['inicial'] and context['final']:
        recibo_passagem=recibo_passagem.filter(data_recibo__gte=context['inicial']).filter(data_recibo__lte=context['final'])

    if context['paciente']:
        recibo_passagem=recibo_passagem.filter(paciente=context['paciente'])

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['data']=datetime.today().strftime('%d/%m/%Y')

    total=0
    qta_passagem=0
    for r in recibo_passagem:
            total+=r.valor_total_passagem()
            qta_passagem+=r.qta_passagem()
    

    context['qta_recibo_passagem']= recibo_passagem.count()
    context['recibos_tfds']=recibo_passagem
    context['total_recibo']=total
    context['qta_passagem']=qta_passagem

    """  context['total_diarias']=total
    context['total_reembolsos']=total_reembolsos """
 

    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('tfds/recibo_passagem/relatorio_recibo_passagem_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

@has_role_decorator(['coordenador','tfd','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def relatorio_recibo_passagem(request):
    context={}
    recibos=ReciboPassagemTFD.objects.select_related('paciente').all()
    paginator = Paginator(recibos,10)  
    page_number = request.GET.get("page")
    recibos= paginator.get_page(page_number)

    if request.method == 'POST':
        form=RelatorioReciboPassagemForm(request.POST or None)

        if form.is_valid():
            context['inicial']=form.cleaned_data.get('data_inicial')
            context['final']=form.cleaned_data.get('data_final')
            context['paciente']=form.cleaned_data.get('pacientes')

            return relatorio_recibo_passagem_pdf(request,context)
           
    else:
        form=RelatorioReciboPassagemForm(request.POST or None)

    return render(request,'tfds/recibo_passagem/relatorio_recibo_passagem.html',{'form':form,'recibos':recibos})