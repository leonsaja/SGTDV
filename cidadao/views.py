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
    cidadao=Cidadao.objects.get(id=id)
    
    if not cidadao:
        return Http404()
    
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

    cidadao=Cidadao.objects.get(id=id)
    
    if not cidadao:
        raise Http404()
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
    paginate_by=4


    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoListView,self).get_queryset(*args, **kwargs)
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
       
        if search_nome_cpf and data:
            queryset=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf)).filter(dt_nascimento__iexact=data).order_by('-nome_completo')
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('endereco','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf)).order_by('-nome_completo')
            return queryset
        
        elif data:
            queryset=qs.select_related('endereco','microarea').filter(dt_nascimento__iexact=data).order_by('-nome_completo')
            return queryset
    
        qs = qs.none()
        return qs
