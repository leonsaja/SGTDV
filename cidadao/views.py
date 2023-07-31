from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from cidadao.forms.cidadao_form import CidadaoForm, EnderecoForm
from cidadao.models import Cidadao


def cidadaoCreate(request):
    if request.method == 'POST':
        form=CidadaoForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
    
        if form.is_valid() and form_endereco.is_valid():
          
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            return redirect('cidadao:list-cidadao')
    
    form=CidadaoForm(request.POST or None)
    form_endereco=EnderecoForm(request.POST or None)      
    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

def cidadaoUpdate(request,id):

    cidadao=get_object_or_404(Cidadao,id=id)
    
    
    if request.method =='POST':
        form=CidadaoForm(request.POST or None, instance=cidadao)
        form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            cidadao_form=form.save(commit=False)
            endereco_form=form_endereco.save()
            cidadao_form.endereco=endereco_form
            cidadao_form.save()
            return redirect('cidadao:list-cidadao')
        
    form=CidadaoForm(request.POST or None,instance=cidadao)
    form_endereco=EnderecoForm(request.POST or None, instance=cidadao.endereco)

    return render(request,'cidadao/form_cidadao.html',{'form':form,'endereco':form_endereco})

def cidadaoDelete(request,id):

    cidadao=get_object_or_404(Cidadao,id=id)

    try:
        cidadao.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
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
   

    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('endereco','microarea').order_by('nome_completo')[:5]
        return qs

class CidadaoSearchListView(ListView):
    
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=10


    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoSearchListView,self).get_queryset(*args, **kwargs)

        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_nome_mae=self.request.GET.get('search_nome_mae',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)

       
        if search_nome_cpf and search_nome_mae and search_dt_nascimento:
            queryset=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(nome_mae__icontains=search_nome_mae)\
                .filter(dt_nascimento__iexact=search_dt_nascimento)
            return queryset
        
        elif search_nome_cpf  and search_dt_nascimento:
            queryset=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(dt_nascimento__iexact=search_dt_nascimento).order_by('-nome_completo')
            return queryset
        
        elif search_nome_mae and search_dt_nascimento:
            queryset=qs.select_related('endereco','microarea')\
                .filter(nome_mae__icontains=search_nome_mae)\
                    .filter(dt_nascimento__iexact=search_dt_nascimento)
            return queryset              
        
        elif search_nome_cpf:
            queryset=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
            return queryset
        
        elif search_nome_mae:
            queryset=qs.select_related('endereco','microarea').filter(nome_mae__icontains=search_nome_mae).order_by('-nome_completo')
            return queryset
        
        
        elif search_dt_nascimento:
            print('teste 6',search_dt_nascimento)
            queryset=qs.select_related('endereco','microarea').filter(dt_nascimento__iexact=search_dt_nascimento).order_by('-nome_completo')
            return queryset
            
        else:
            qs=qs.select_related('endereco','microarea').all()
            return qs
