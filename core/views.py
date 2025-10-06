from django.http import JsonResponse
from django.shortcuts import render
import locale
from django.db.models import Q
from django.http import JsonResponse
import json
from cidadao.models import Cidadao
from despesas.models import Diaria,Reembolso
from especialidades.models import Especialidade, PacienteEspecialidade
from tfds.models import ReciboTFD
from transportes.models import Viagem,RegistroTransporte
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from especialidades.models import AtendimentoEspecialidade
from datetime import datetime
from core.models import Agenda
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from core.form import AgendamentoForm
from django.shortcuts import render,redirect

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
   context['qta_cadastro_incompleto']=Cidadao.objects.select_related('endereco','microarea').filter(Q(cns=None)).count() 
   especialidades=Especialidade.objects.filter(paciente_especialidades__isnull=False).distinct()
   
   paginator = Paginator(especialidades,10)  
   page_number = request.GET.get("page")
   context['page_obj']= paginator.get_page(page_number)
  
   #Gasto com TFDs
   gastos_tfd_por_mes = ReciboTFD.objects.annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        total_gasto_mes=Sum('total_gasto')
    ).exclude(status='3').order_by('mes')
    
    # Prepara os dados para o Chart.js
   labels_tfd = [item['mes'].strftime('%B de %Y') for item in gastos_tfd_por_mes]
   valores_tfd = [float(item['total_gasto_mes']) if item['total_gasto_mes'] else 0 for item in gastos_tfd_por_mes]
    
   context['labels_tfd'] = labels_tfd
   context['valores_tfd'] =  valores_tfd 
   """
   #Gasto com Diárias
   gastos_diarias_por_mes = Diaria.objects.annotate(
       mes=TruncMonth('data_diaria')
   ).values('mes').annotate(
       total_diarias=Sum('total')
   ).exclude(status='3').order_by('mes')   
   # Agrupa os reembolsos por mês e soma os valores
   # A data do reembolso está indiretamente ligada à Diaria,
   # então usamos a data da Diaria
   gastos_reembolsos_por_mes = Reembolso.objects.annotate(
       mes=TruncMonth('reembolso_principal__diaria__data_diaria')
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
   context['valores_reembolsos']=valores_reembolsos"""
    
   return render(request,'home.html',context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
"""
def calendario_view(request):
    form = AgendamentoForm()
    return render(request, 'agenda.html', {'form': form})

def agendamento_criar_ajax(request):
    print('criar')
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            novo_agendamento = form.save()
            # Retorna uma resposta JSON com o ID e os dados do novo evento
            return JsonResponse({
                'status': 'success',
                'id': novo_agendamento.pk,
                'title': novo_agendamento.title,
                'start_time': novo_agendamento.start_time,
                'end_time': novo_agendamento.end_time,
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

def agendamentos_json(request):
    print('teste213')
    start_str = request.GET.get('start', None)
    end_str = request.GET.get('end', None)

    if start_str and end_str:
        start_str = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end_str = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        eventos = Agenda.objects.filter(start_time__gte=start_str, end_time__lte=end_str)
        lista_eventos = []
        for evento in eventos:
            lista_eventos.append({
                'title': evento.title,
                'start_time': evento.start_time.isoformat(),
                'end_time': evento.end_time.isoformat(),
            })
            print(lista_eventos)
        
        return JsonResponse(lista_eventos, safe=False)
            
    return JsonResponse([])

"""