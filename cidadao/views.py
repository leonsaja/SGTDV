from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from cidadao.forms.cidadao_form import CidadaoForm, EnderecoForm
from cidadao.models import Cidadao
from django.contrib.messages import constants
from django.contrib import messages

def cidadao_create(request):
    if request.method == 'POST':
        form=CidadaoForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
    
        if form.is_valid() and form_endereco.is_valid():
          
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            messages.add_message(request,constants.SUCCESS,'cadastro realizado com sucesso')

            return redirect('cidadao:list-cidadao')
    
    form=CidadaoForm(request.POST or None)
    form_endereco=EnderecoForm(request.POST or None)      
    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

def cidadao_update(request,id):

    cidadao=get_object_or_404(Cidadao,id=id)
    
    
    if request.method =='POST':
        form=CidadaoForm(request.POST or None, instance=cidadao)
        form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            cidadao_form=form.save(commit=False)
            endereco_form=form_endereco.save()
            cidadao_form.endereco=endereco_form
            cidadao_form.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('cidadao:list-cidadao')
        
    form=CidadaoForm(request.POST or None,instance=cidadao)
    form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)

    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

def cidadao_delete(request,id):

    cidadao=get_object_or_404(Cidadao,id=id)

    try:
        cidadao.delete()
        messages.add_message(request, constants.SUCCESS ,"Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request, constants.ERROR ,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('cidadao:list-cidadao')

class CidadaoDetailView(DetailView):
    model=Cidadao
    template_name='cidadao/detail_cidadao.html'


    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context[ 'paciente']=Cidadao.objects.select_related('endereco','microarea').get(pk=self.kwargs['pk'])
        
        return context

class CidadaoListView(ListView):
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=10
   

    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('endereco','microarea').order_by('nome_completo')
        return qs

class CidadaoSearchListView(ListView):
    
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=10


    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoSearchListView,self).get_queryset(*args, **kwargs)

        search_nome_cpf_cns=self.request.GET.get('search_nome_cpf',None)
        search_nome_mae=self.request.GET.get('search_nome_mae',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)

        if search_nome_cpf_cns:
            qs=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf_cns)| Q(cpf__icontains=search_nome_cpf_cns)|Q(cns__icontains=search_nome_cpf_cns))
              
        if search_nome_mae:
            qs=qs.select_related('endereco','microarea').filter(nome_mae__icontains=search_nome_mae)
        
        if search_dt_nascimento:
            qs=qs.select_related('endereco','microarea').filter(dt_nascimento__iexact=search_dt_nascimento)

        return qs
