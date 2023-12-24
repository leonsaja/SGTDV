from django.shortcuts import render

from cidadao.models import Cidadao
from despesas.models import Diaria
from especialidades.models import Especialidade, PacienteEspecialidade
from tfds.models import ReciboTFD
from transportes.models import Viagem
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
   context={}
   context['qta_cidadao']=Cidadao.objects.select_related('endereco','microarea').count()
   context['qta_diaria']=Diaria.objects.select_related('profissional').count()
   context['qta_viagens']=Viagem.objects.select_related('carro','motorista').count()
   context['qta_recibo_tfd']=ReciboTFD.objects.select_related('paciente').count()

   especialidade=Especialidade.objects.all()

 

   return render(request,'home.html',context)
