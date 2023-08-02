from django.shortcuts import render

from cidadao.models import Cidadao
from despesas.models import Diaria
from especialidades.models import Especialidade, PacienteEspecialidade
from tfds.models import ReciboTFD
from transportes.models import Viagem


def home(request):
   context={}
   context['qta_cidadao']=Cidadao.objects.count()
   context['qta_diaria']=Diaria.objects.count()
   context['qta_viagens']=Viagem.objects.count()
   context['qta_recibo_tfd']=ReciboTFD.objects.count()

   especialidade=Especialidade.objects.all()

 

   return render(request,'home.html',context)
