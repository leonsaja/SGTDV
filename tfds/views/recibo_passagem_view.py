from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from tfds.forms.form_recibo_passagem_tfd import ReciboPassagemTFDForm
from tfds.models import ReciboPassagemTFD


class ReciboPassagemTFDCreateView(CreateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')

class ReciboPassagemTFDUpdateView(UpdateView):
    model=ReciboPassagemTFD
    form_class=ReciboPassagemTFDForm
    template_name='recibo_passagem_tfd/form_recibo_passagem.html'
    success_url=reverse_lazy('tfds:list-recibo_passagem')


class ListReciboPassagemTFDView(ListView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/list_recibos_passagens.html'
    context_object_name='recibos'
    paginate_by=1

    
    def get_queryset(self, *args, **kwargs):
        qs = super(ListReciboPassagemTFDView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_data_recibo=self.request.GET.get('data',None)
        print(search_data_recibo,'teste10')

        if search_nome_cpf and search_data_recibo:
            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
                .filter(data_recibo__iexact=search_data_recibo)
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('paciente','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))
            return queryset
        
        elif search_data_recibo:
             print(search_data_recibo,'30' )
             queryset=qs.select_related('paciente','acompanhante').filter(data_recibo__iexact=search_data_recibo)
             return queryset
        
        else:
            qs = qs.select_related('paciente','acompanhante').order_by('-id')[:3]
            return qs
    

class DetailReciboPassagemTFD(DetailView):
    model=ReciboPassagemTFD
    template_name='recibo_passagem_tfd/detail_recibo_passagem.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibo"] =ReciboPassagemTFD.objects.select_related('paciente', 'acompanhante').get(id=self.kwargs['pk'])
       
        return context
    



     
                                                                                                                                                                                                                                              
