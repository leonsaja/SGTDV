from django.shortcuts import render
from relatorios.forms.registro_transporte_form import RelatorioRegistroTransporteForm
from transportes.models import RegistroTransporte
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def relatorio_registro_transporte_pdf(request,context):
    transportes=RegistroTransporte.objects.select_related('paciente','carro').all()
   
    if context['inicial'] and context['final']:
        transportes=transportes.filter(dt_atendimento__gte=context['inicial']).filter(dt_atendimento__lte=context['final'])
        context['qta_atend_carro_proprio_paciente']=transportes.filter(carro__forma_atend='1').count()


        context['qta_atend_zona_rural']=transportes.filter(atend_zona_rural='1').count()
        context['qta_atendimento_eventual']=transportes.filter(tipo_atend='1').count()
        context['qta_atendimento_rotineiro']=transportes.filter(tipo_atend='2').count()
        

        #Quantidade pessoas que nao compareceu
        total=0
        total=transportes.filter(status='2').count() + transportes.filter(status='3').count()+transportes.filter(status='4').count()
        context['qta_paciente_nao_foi_consulta']=total

        #Veiculo de Proprio
        context['qta_atend_carro_proprio_paciente']=transportes.filter(carro__forma_atend='1').count()
        context['qta_atend_carro_proprio_acompanhante']=transportes.filter(acompanhante='1').filter(carro__forma_atend='1').count()
        context['total_atend_carro_propio']=context['qta_atend_carro_proprio_paciente']+context['qta_atend_carro_proprio_acompanhante']

        #Veiculo do Consorcio
        context['qta_atend_carro_consorcio_paciente']=transportes.filter(carro__forma_atend='2').count()
        context['qta_atend_carro_consorcio_acompanhante']=transportes.filter(acompanhante='1').filter(carro__forma_atend='2').count()
        context['total_atend_carro_consorcio']=context['qta_atend_carro_consorcio_paciente']+context['qta_atend_carro_consorcio_acompanhante']
        
        #Procedimento do Sia
        
        total_proced_paciente=0
        total_proced_acompanhante=0

        for r in transportes:
            if r.quant_proced_acompanhante:
                total_proced_paciente+=r.quant_proced_paciente
                total_proced_acompanhante+=r.quant_proced_acompanhante
            else:
                total_proced_paciente+=r.quant_proced_paciente 
                
        context['qta_proced_paciente']=total_proced_paciente
        context['qta_proced_acompanhante']=total_proced_acompanhante
        context['total_procedimento']=context['qta_proced_paciente']+context['qta_proced_acompanhante']

        #Data
        context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
        context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')

        context['data']=datetime.today().strftime('%d/%m/%Y')

        context['qta_registro_transporte']= transportes.count()

        response = HttpResponse(content_type='application/pdf')
        html_string = render_to_string('transporte/registro_transporte/relatorio_registro_transporte_pdf.html',context)
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
        return response
    
    else:
        messages.add_message(request,constants.ERROR,'Data inicial e Data final são Campos o obrigatório')
        return render(request,'transporte/registro_transporte/relatorio_registro_transporte.html',context)
  
@login_required      
@has_role_decorator(['coordenador','secretario','regulacao'],redirect_url='usuarios:acesso_negado')
def relatorio_registro_transporte(request):
    context={}
    transportes= RegistroTransporte.objects.select_related('paciente','carro').order_by('-created_at').all()
    
    if request.method == 'POST':
        form=RelatorioRegistroTransporteForm(request.POST or None)

        if form.is_valid():
            context['inicial']=form.cleaned_data.get('data_inicial')
            context['final']=form.cleaned_data.get('data_final')
            context['paciente']=form.cleaned_data.get('pacientes')
            context['atend_zona_rural']=form.cleaned_data.get('atend_zona_rural')
            context['status']=form.cleaned_data.get('status')
            context['tipo_atendimento']=form.cleaned_data.get('tipo_atendimento')
            context['classificacao']=form.cleaned_data.get('classificacao')
            context['form']=form
            return relatorio_registro_transporte_pdf(request,context)
           
    else:
        form=RelatorioRegistroTransporteForm(request.POST or None)
        
    paginator = Paginator(transportes,10)  
    page_number = request.GET.get("page")
    context['page_obj']= paginator.get_page(page_number)
    
    context['form']=form

    return render(request,'transporte/registro_transporte/relatorio_registro_transporte.html',context)