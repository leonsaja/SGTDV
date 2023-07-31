from django.shortcuts import render
from cidadao.models import Cidadao
from despesas.models import Diaria
from transportes.models import Viagem
from tfds.models import ReciboTFD


def home(request):
   context={}
   context['qta_cidadao']=Cidadao.objects.count()
   context['qta_diaria']=Diaria.objects.count()
   context['qta_viagens']=Viagem.objects.count()
   context['qta_recibo_tfd']=ReciboTFD.objects.count()

   return render(request,'home.html',context)
