
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from weasyprint import HTML
from django.shortcuts import render
from despesas.models import Diaria
from relatorios.forms.diaria_form import RelatorioDiariaForm
from datetime import datetime
from django.db.models import Q
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from profissionais.models import Profissional
from io import BytesIO
from datetime import date


def relatorio_diaria_pdf(request,context):
    diarias=Diaria.objects.select_related('profissional').filter(data_diaria__gte=context['inicial']).filter(data_diaria__lte=context['final']).exclude(status='3')
    
    if context['profissional']:
        diarias=diarias.filter(profissional=context['profissional'])
  

    start_date = context['inicial']
    end_date = context['final']

    if context['tipo_relatorio'] == '3':
        motoristas = Profissional.objects.filter(cargo='7')

        motoristas_com_dados = motoristas.annotate(
            total_diarias=Count('profissionais', filter=Q(profissionais__data_diaria__range=(start_date, end_date))),
            soma_valores=Sum('profissionais__total', filter=Q(profissionais__data_diaria__range=(start_date, end_date)))
        ).exclude(total_diarias=0).order_by('nome_completo')

        total_geral_diarias = Diaria.objects.filter(profissional__cargo='7', data_diaria__range=(start_date, end_date)).count()
        soma_total_valores = Diaria.objects.filter(profissional__cargo='7', data_diaria__range=(start_date, end_date)).aggregate(Sum('total'))['total__sum']

        context['motoristas'] = motoristas_com_dados
        context['total_geral_diarias'] = total_geral_diarias
        context['soma_total_valores'] = soma_total_valores



    context['qta_diarias']= diarias.count()
    context['qta_reembolsos']=diarias.filter(reembolso='1').count()
        
    total=0
    total_reembolsos=0
   

    context['inicial']=datetime.strptime(context['inicial'],'%Y-%m-%d').strftime('%d/%m/%Y')
    context['final']=datetime.strptime(context['final'],'%Y-%m-%d').strftime('%d/%m/%Y')
    

    context['data']=datetime.today().strftime('%d/%m/%Y') 
    context['diarias']=diarias

  
    for d in diarias:
        total+=d.total

        for r in d.reembolsos.all():
            if r.valor_desp:
                total_reembolsos+=r.valor_desp
    

    
    context['total_diarias']=total
    context['total_reembolsos']=total_reembolsos
    
    buffer = BytesIO()
    html_string = render_to_string('diaria/relatorio_diaria_pdf.html',context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Relatorio_Diarias_{date.today().strftime("%d/%m/%Y")}.pdf"'

    return response

@has_role_decorator(['secretario','digitador','coordenador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def relatorio_diaria(request):
    context={}
    diarias=Diaria.objects.select_related('profissional').order_by('-created_at')
    paginator = Paginator(diarias,10)  
    page_number = request.GET.get("page")
    diarias= paginator.get_page(page_number)
  
    if request.method == 'POST':
        form=RelatorioDiariaForm(request.POST or None)

        if form.is_valid():
          context['inicial']=form.cleaned_data.get('data_inicial')
          context['final']=form.cleaned_data.get('data_final')
          context['profissional']=form.cleaned_data.get('profissionais')
          context['tipo_relatorio']=form.cleaned_data.get('tipo_relatorio')
      
          return relatorio_diaria_pdf(request,context)

    else:
        form=RelatorioDiariaForm(request.POST or None)    
        
    return render(request,'diaria/relatorio_diaria.html',{'form':form,'diarias':diarias})           
