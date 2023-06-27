from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from despesas.models import Diaria
from profissionais.forms.form_profissional import (EnderecoForm,
                                                   ProfissionalForm)

from .models import Profissional


def profissionalCreate(request):

    if request.method == 'POST':
        form=ProfissionalForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
       
        if form.is_valid() and form_endereco.is_valid():
            
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            
            return redirect('profissionais:list-profissional')
        
    form=ProfissionalForm(request.POST or None)
    form_endereco=EnderecoForm(request.POST or None)
    
    return render(request,'profissional/form_profissional.html',{'form':form,'form_endereco':form_endereco})

def profissionalUpdate(request,id):
    profissional=Profissional.objects.get(id=id)
    
    if not profissional:
        raise Http404()

    if request.method == 'POST':
        form=ProfissionalForm(request.POST or None, instance=profissional)
        form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            print('profissionais is valido')
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            return redirect('profissionais:list-profissional')
        
    form=ProfissionalForm(request.POST or None, instance=profissional)
    form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
    return render(request,'profissional/form_profissional.html',{'form':form,'form_endereco':form_endereco})

def profissionalDelete(request, id):
    profissional=Profissional.objects.get(id=id)

    if not profissional:
        raise Http404()
    try:
        profissional.delete()
    except ProtectedError:
        messages.error(request, "Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('profissionais:list-profissional')

class ProfissionalDetailView(DetailView):

    model=Profissional
    template_name='profissional/detail_profissional.html'
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['profissional']= Profissional.objects.select_related('endereco','microarea','estabelecimento').get(id=self.kwargs['pk'])
        
        return context

class ProfissionalListView(ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
    context_object_name='profissionais'
    paginate_by=2

    def get_queryset(self, *args, **kwargs):
        qs = super(ProfissionalListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        search_dt_nascimento=self.request.GET.get('search_dt_nascimento',None)
        
        if search_nome_cpf and search_dt_nascimento:
            queryset=qs.select_related('endereco','estabelecimento','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(dt_nascimento__iexact=search_dt_nascimento)
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.select_related('endereco','estabelecimento','microarea').filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
            return queryset
        
        elif search_dt_nascimento:
             queryset=qs.select_related('endereco','estabelecimento','microarea').filter(dt_nascimento__iexact=search_dt_nascimento).order_by('-nome_completo')
             return queryset
        
        else:
            qs = qs.select_related('endereco','estabelecimento','microarea').order_by('-id')[:3]
        return qs

#Profissional Diaria 
class ProfissionalDiariaListView(ListView):
    model=Profissional
    template_name='profissional/diarias_profissional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profissional=Profissional.objects.select_related('endereco','microarea','estabelecimento').get(id=self.kwargs['pk'])
        context["diarias"] = Diaria.objects.select_related('profissional').filter(profissional__id=profissional.id)
        context['profissional']=profissional
        print(context['diarias'])
        return context
    
