from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from profissionais.forms.form_profissional import (EnderecoForm,
                                                   ProfissionalForm)

from .models import Profissional


def profissionalCreate(request):
  
    form=ProfissionalForm()
    form_endereco=EnderecoForm()
   
    context={
            'title':'Cadastro de Profissional',
            'form_title':'Dados Pessoais',
            'endereco_title':'Endereco',  
    }  
     
    if request.method == 'POST':
       
        form=ProfissionalForm(request.POST or None)
        form_endereco=EnderecoForm(request.POST or None)
       
        
        if form.is_valid() and form_endereco.is_valid():
            print('teste request5')
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            
            return redirect('profissionais:list-profissional')
            
        else:
            form=ProfissionalForm(request.POST or None)
            form_endereco=EnderecoForm(request.POST or None)
   
    context['form']=form
    context['form_endereco']=form_endereco       
    return render(request,'profissional/form_profissional.html',context,)

def profissionalUpdate(request,id):
    profissional=Profissional.objects.get(id=id)
    
    if not profissional:
        raise Http404()
    
    form=ProfissionalForm(request.POST or None, instance=profissional)
    form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
    
    if request.method == 'POST':
        form=ProfissionalForm(request.POST or None, instance=profissional)
        form_endereco=EnderecoForm(request.POST or None, instance=profissional.endereco)
        
        if form.is_valid() and form_endereco.is_valid():
            forms=form.save(commit=False)
            form_end=form_endereco.save()
            forms.endereco=form_end
            forms.save()
            return redirect('profissionais:list-profissional')
        
    context={
            'title':'Edição de Profissional',
            'form_title':'Dados Pessoais',
            'endereco_title':'Endereco',  
            'form':form,
            'form_endereco':form_endereco
    }  
    return render(request,'profissional/form_profissional.html',context)

class ProfissionalListView(ListView):
    model=Profissional
    template_name='profissional/list_profissionais.html'
   
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
       
        context={
            'nome_modal':'Profissional',
            'profissionais':Profissional.objects.all().order_by('-id')
            
        }
        return context
    
    
class ProfissionalDetailView(DetailView):
    model=Profissional
    template_name='profissional/detail_profissional.html'
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
       
        context={
            'title':'Detalhe do Cadastro',
            'form_title':'Dados Pessoais',
            'endereco_title':'Endereco',
            'profissional': Profissional.objects.get(pk=self.kwargs['pk'])
        }
        return context
    
class ProfissionalDeleteView(DeleteView):
    model=Profissional
    success_url=reverse_lazy('profissionais:list-profissional')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)
    
class ProfissionalDiariasListView(ListView):
    model=Profissional
    template_name='profissional/diarias_profissional.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profissional=Profissional.objects.get(pk=self.kwargs['pk'])
        context["diarias"] = profissional.profissionais.all()
        context['profissional']=profissional
        print(context['diarias'])
        return context
    
