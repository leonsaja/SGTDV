from django.shortcuts import render
from django.urls import reverse_lazy
from relatorios.forms.viagem_form import RelatorioViagemForm
from transportes.models import Viagem
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
from io import BytesIO
from datetime import date
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator

def relatorio_viagem_pdf(request,context):
    viagens=Viagem.objects.select_related('motorista','carro').all()
   
    if context['inicial'] and context['final']:
        viagens=viagens.filter(data_viagem__gte=context['inicial']).filter(data_viagem__lte=context['final'])
      
        if context['profissional']:
            viagens=viagens.filter(motorista=context['profissional'])

        if context['status']:
            viagens=viagens.filter(status=context['status'])

        total_pessoas=0
        for v in viagens:
           total_pessoas+=v.qta_pessoas()

        context['qta_pessoas_transportados']=total_pessoas
    
        #Data
        context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
        context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
        context['data']=datetime.today().strftime('%d/%m/%Y')

        #total de viagem do periodo
        context['qta_registro_viagens']= viagens.count()

        context['viagens']=viagens.all()
        
        buffer = BytesIO()
        html_string = render_to_string('transporte/viagem/relatorio_viagem_pdf.html',context)
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Relatorio_Viagens_{date.today().strftime("%d/%m/%Y")}.pdf"'
        return response

    
    else:
        messages.add_message(request,constants.ERROR,'Data inicial e Data final são Campos o obrigatório')
        return render(request,'transporte/viagem/relatorio_viagem.html',context)
        
@has_role_decorator(['regulacao','recepcao','coordenador','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def relatorio_viagem(request):
    context={}
    viagens=Viagem.objects.select_related('carro','motorista').all().order_by('-data_viagem')
    
    if request.method == 'POST':
        form=RelatorioViagemForm(request.POST or None)

        if form.is_valid():
            context['inicial']=form.cleaned_data.get('data_inicial')
            context['final']=form.cleaned_data.get('data_final')
            context['status']=form.cleaned_data.get('status')
            context['profissional']=form.cleaned_data.get('profissionais')

            context['form']=form
            return relatorio_viagem_pdf(request,context)
           
    else:
        form=RelatorioViagemForm(request.POST or None)

    return render(request,'transporte/viagem/relatorio_viagem.html',{'form':form,'viagens':viagens})