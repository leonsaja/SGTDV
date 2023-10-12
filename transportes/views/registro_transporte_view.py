from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DeleteView,DetailView
from transportes.models import RegistroTransporte
from transportes.forms.registro_transporte_form import RegistroTransporteForm
from django.contrib.messages.views import SuccessMessageMixin

class RegistroTransporteCreateView(SuccessMessageMixin,CreateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro realizado com sucesso'

class RegistroTransporteUpdateView(SuccessMessageMixin,UpdateView):
    model =RegistroTransporte
    form_class=RegistroTransporteForm
    template_name='registro_transporte/form_registro_transporte.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Cadastro alterado  com sucesso'
           
class RegistroTransporteListView(ListView):
    model=RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    paginate_by=10
    
    
    def get_queryset(self, *args, **kwargs):
        qs = super(RegistroTransporteListView,self).get_queryset(*args, **kwargs)
        qs = qs.select_related('paciente','carro').order_by('-created_at').all()
        return qs
       
class RegistroTransporteDetailView(DetailView):
    model=RegistroTransporte
    context_object_name='transporte'
    template_name='registro_transporte/detail_registro_transporte.html'

class RegistroTransporteDeleteView(SuccessMessageMixin, DeleteView):
    model=RegistroTransporte
    success_url=reverse_lazy('transportes:list-regis-transporte')
    success_message='Registro excluido com sucesso'
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

class RegistroTransporteSearchListView(ListView):
    model=RegistroTransporte
    template_name='registro_transporte/list_registro_transporte.html'
    context_object_name='transportes'
    paginate_by=10

    def get_queryset(self):
        qs=super().get_queryset()
        
        nome_paciente=self.request.GET.get('nome_paciente',None)
        dt_atendimento=self.request.GET.get('data',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        
    
        if nome_paciente and dt_atendimento and placa_carro:
            queryset=qs.select_related('paciente','carro').filter(paciente__nome_completo__icontains=nome_paciente,\
                dt_atendimento=dt_atendimento,carro=placa_carro).order_by('-created_at')
        
        elif nome_paciente and dt_atendimento:
            queryset=qs.select_related('paciente','carro').filter(paciente__nome_completo__icontains=nome_paciente,\
                dt_atendimento=dt_atendimento).order_by('-created_at')
              
        elif dt_atendimento and placa_carro:
            queryset=qs.select_related('paciente','carro').filter(dt_atendimento=dt_atendimento,\
                carro__placa__icontains=placa_carro).order_by('-created_at')
            
        elif nome_paciente:
            print('teste3',nome_paciente)
            queryset=qs.select_related('paciente','carro').\
                filter(paciente__nome_completo__icontains=nome_paciente).order_by('-created_at')
                
        elif dt_atendimento:
            queryset=qs.select_related('paciente','carro').filter(dt_atendimento=dt_atendimento)
            
        elif placa_carro:
            print('teste6',placa_carro)
            queryset=qs.select_related('paciente','carro').filter(carro__placa__icontains=placa_carro)
            
            
        else:
            queryset=qs.select_related('paciente','carro').all().order_by('-created_at')
    
        return queryset
    
    