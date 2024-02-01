from django.http import JsonResponse
from django.shortcuts import render

from cidadao.models import Cidadao
from despesas.models import Diaria
from especialidades.models import Especialidade, PacienteEspecialidade
from tfds.models import ReciboTFD
from transportes.models import Viagem
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def home(request):
   context={}
   context['qta_cidadao']=Cidadao.objects.select_related('endereco','microarea').count()
   context['qta_diaria']=Diaria.objects.select_related('profissional').count()
   context['qta_viagens']=Viagem.objects.select_related('carro','motorista').count()
   context['qta_recibo_tfd']=ReciboTFD.objects.select_related('paciente').count()

   especialidade=Especialidade.objects.all()

 

   return render(request,'home.html',context)

def relatorio_despesas(request):
    d = Diaria.objects.all()
    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = datetime.now().month + 1
    ano = datetime.now().year
    
    for i in range(12): 
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        y=0
        for i in d:
            print('data_diaria 1',i.data_diaria.month)
            if i.data_diaria.month == mes and i.data_diaria.year == ano:
                
                y=sum([i.total])
        
        labels.append(meses[mes-1])
        data.append(y)
        cont += 1

    data_json = {'data': data[::-1], 'labels': labels[::-1]}
    print('data',data_json)
    return JsonResponse(data_json)