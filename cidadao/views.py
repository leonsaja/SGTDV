from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

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
       
        context={
            'title':'Detalhe do Cadastro',
            'form_title':'Dados Pessoais',
            'endereco_title':'Endereco',
            'paciente': Cidadao.objects.get(pk=self.kwargs['pk'])
        }
        return context

class CidadaoListView(ListView):
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    



""" 
    class CidadaoDeleteView(DeleteView):
    model=Cidadao
    success_url=reverse_lazy('cidadao:list-cidadao')
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)
    """


""" 

class CidadaoEditView(UpdateView):

    form_class=form_cidadao.CidadaoForm
    model=Cidadao
    context_object_name='form'
    success_url='cidadao:list-cidadao'
    template_name='cidadao/edit_cidadao.html'

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        form_class=self.get_form_class()
        form=self.get_form(form_class)

        endereco=form_cidadao.CidadaoForm(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form,endereco=endereco))
    
    def post(self, request,*args, **kwargs):
        self.object=self.get_object()
        form_class=self.get_form_class()
        form=self.get_form(form_class)
        
        endereco=form_cidadao.CidadaoForm(request.POST)
        
        if(form.is_valid() and endereco.is_valid()):
            return self.form_valid(form,endereco)
        else:
            return self.form_invalid(form,endereco)  
        
    def form_valid(self,form, endereco):
        endereco_form=endereco.save()
        self.object=form.save(commit=False)
        self.object.instance=endereco_form
        self.object.save()
        
        
    def form_invalid(self,form, endereco):
        return self.get_context_data(form=form,endereco=endereco)
    
   """
    
   
        

""" 
class AddCidadao(CreateView):
    model = Cidadao
    form_class=form_cidadao.Cidadao
    template_name='cidadao/form_cidadao.html'
    form_class_add=form_cidadao.EnderecoForm
    
    def get(self, request, *args, **kwargs):
        context={
            'form':self.form_class,
        }
        return render(request,self.template_name,context)
    
    
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['form']=form_cidadao.CidadaoForm()
        context['endereco']=form_cidadao.EnderecoForm()
        return  context
 """