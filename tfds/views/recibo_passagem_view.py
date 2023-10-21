
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from django.contrib.messages.views import SuccessMessageMixin

from tfds.forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from tfds.models import ReciboPassagemTFD

from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

class ReciboPassagemCreateView(SuccessMessageMixin,CreateView):
    
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')
    success_message='Cadastro realizado com sucesso'

class ReciboPassagemUpdateView(SuccessMessageMixin,UpdateView):
    
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')
    context_object_name='recibo_passagem'
    success_message='Dados atualizado com sucesso'
    
class ReciboPassagemListView(ListView):

    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'
    context_object_name='recibos'
    ordering='-created_at'
    paginate_by=10
    queryset=ReciboPassagemTFD.objects.select_related('paciente').all()
   
class ReciboPassagemSearchListView(ListView):
    
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'
    context_object_name='recibos'
    paginate_by=10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboPassagemSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_data_recibo=self.request.GET.get('data',None)

        if search_nome_cpf and search_data_recibo:
            qs=qs.select_related('paciente').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
                .filter(data_recibo__iexact=search_data_recibo)
            
        
        elif search_nome_cpf:
            qs=qs.select_related('paciente').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)|\
                Q(paciente__cpf__icontains=search_nome_cpf))
          
        
        elif search_data_recibo:     
             qs=qs.select_related('paciente').filter(data_recibo__iexact=search_data_recibo)
        
        return qs
        
class ReciboPassagemDetailView(DetailView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/detail_recibo_passagem.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibo"] =ReciboPassagemTFD.objects.select_related('paciente').get(id=self.kwargs['pk'])
       
        return context

class ReciboPassagemDeleteView(SuccessMessageMixin,DeleteView):
    model=ReciboPassagemTFD
    success_url=reverse_lazy('tfds:list-recibo_passagem')
    success_message='Registro excluido com sucesso'

    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)

                                                                                                                                                                                                                                                 
def reciboPassagemPdf(request,id):

    recibo_passagem=get_object_or_404(ReciboPassagemTFD,id=id)
    context={}

    context['recibo_passagem']= ReciboPassagemTFD.objects.select_related('paciente').get(id=recibo_passagem.id)
   
    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('recibo_passagem_tfd/pdf_recibo_passagem.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)


    return response
