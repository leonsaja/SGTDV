from django.http import JsonResponse
from django.shortcuts import render
import locale
from cidadao.models import Cidadao
from despesas.models import Diaria,Reembolso
from especialidades.models import Especialidade, PacienteEspecialidade
from tfds.models import ReciboTFD
from transportes.models import Viagem,RegistroTransporte
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from especialidades.models import AtendimentoEspecialidade
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import TruncMonth

@login_required
def home(request):
   try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
  
   except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'portuguese_brazil')
        except locale.Error:
            pass  # Se não conseguir, usa o padrão do sistema (geralmente inglês)

   context={}
   context['qta_cidadao']=Cidadao.objects.select_related('endereco','microarea').count()
   context['qta_diaria']=Diaria.objects.select_related('profissionals').count()
   context['qta_viagens']=Viagem.objects.select_related('carro','motorista').count()
   context['qta_recibo_tfd']=ReciboTFD.objects.select_related('paciente').count()
   context['qta_registro_transporte']=RegistroTransporte.objects.select_related('paciente','carro').count()
   context['qta_atendimento']=AtendimentoEspecialidade.objects.count()
   context['qta_cadastro_incompleto']=Cidadao.objects.select_related('endereco','microarea').filter(cns=None).count()
   especialidades=Especialidade.objects.all()
   
   paginator = Paginator(especialidades,10)  
   page_number = request.GET.get("page")
   context['page_obj']= paginator.get_page(page_number)
  

   gastos_tfd_por_mes = ReciboTFD.objects.annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        total_gasto_mes=Sum('total_gasto')
    ).order_by('mes')
    
    # Prepara os dados para o Chart.js
   labels_tfd = [item['mes'].strftime('%B de %Y') for item in gastos_tfd_por_mes]
   valores_tfd = [float(item['total_gasto_mes']) if item['total_gasto_mes'] else 0 for item in gastos_tfd_por_mes]
    
   context['labels_tfd'] = labels_tfd
   context['valores_tfd'] =  valores_tfd 
   
   gastos_diarias_por_mes = Diaria.objects.annotate(
       mes=TruncMonth('data_diaria')
   ).values('mes').annotate(
       total_diarias=Sum('total')
   ).order_by('mes')   
   # Agrupa os reembolsos por mês e soma os valores
   # A data do reembolso está indiretamente ligada à Diaria,
   # então usamos a data da Diaria
   gastos_reembolsos_por_mes = Reembolso.objects.annotate(
       mes=TruncMonth('diaria__data_diaria')
   ).values('mes').annotate(
       total_reembolsos=Sum('valor_desp')
   ).order_by('mes')   
   # Para juntar os dados em uma estrutura fácil de usar no template:
   data_dict = {}
   
   for item in gastos_diarias_por_mes:
       mes_ano = item['mes'].strftime('%B %Y') # Ex: "Agosto 2025"
       data_dict[mes_ano] = {'diarias': item['total_diarias'], 'reembolsos': 0}   
   for item in gastos_reembolsos_por_mes:
       mes_ano = item['mes'].strftime('%B %Y')
       if mes_ano in data_dict:
           data_dict[mes_ano]['reembolsos'] = item['total_reembolsos']
       else:
           # Caso haja reembolso sem diária, o que é improvável com sua estrutura
           data_dict[mes_ano] = {'diarias': 0, 'reembolsos': item['total_reembolsos']}   
  
  
   labels = list(data_dict.keys())
   valores_diarias = [item['diarias'] for item in data_dict.values()]
   valores_reembolsos = [item['reembolsos'] for item in data_dict.values()]
  
   context['labels']= labels
   context['valores_diarias']= valores_diarias
   context['valores_reembolsos']=valores_reembolsos
    
   return render(request,'home.html',context)
