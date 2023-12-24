from django.db.models import  Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from tfds.forms.form_recibo_tfd import ReciboTFDForm
from tfds.forms.form_procedimento import ProcedimentoSet
from tfds.models import  ReciboTFD,ProcedimentoSia
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
has_role_decorator(['regulacao'])
def reciboTFD_create(request):
    tfd=ReciboTFD()
    if request.method == 'POST':

        form = ReciboTFDForm(request.POST,instance=tfd,prefix='recibo' )
        formset=ProcedimentoSet(request.POST,instance=tfd,prefix='procedimento')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso')
            return redirect('tfds:list-recibo_tfd')

    form = ReciboTFDForm(request.POST or None,instance=tfd,prefix='recibo')
    formset=ProcedimentoSet(request.POST or None,instance=tfd,prefix='procedimento')
    
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset})

has_role_decorator(['regulacao'])  
def reciboTFD_update(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=ReciboTFDForm(request.POST, instance=recibo_tfd,prefix='recibo')
        formset=ProcedimentoSet(request.POST, instance=recibo_tfd,prefix='procedimento')
        if form.is_valid() and formset.is_valid():
           form.save()
           formset.save()
           messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
           return redirect('tfds:list-recibo_tfd')

    form=ReciboTFDForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    formset=ProcedimentoSet(request.POST or None, instance=recibo_tfd,prefix='procedimento')
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset,'recibo_tfd':recibo_tfd})

class ReciboTFDListView(HasRoleMixin,ListView):

    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10
    allowed_roles=['regulacao','secretario','coordenador']

    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('paciente').order_by('-created_at')
        return qs
    
class ReciboTFDSearchListView(HasRoleMixin,ListView):
   
    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10
    allowed_roles=['regulacao','secretario','coordenador']

    
    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
      
        if search_nome_cpf:
            qs=qs.select_related('paciente').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
            .order_by('-data')
           
        if data:
             qs=qs.select_related('paciente').filter(data__iexact=data).order_by('-created_at')
        
        return qs

class ReciboTFDDetailView(HasRoleMixin,DetailView):

    model=ReciboTFD
    template_name='recibo_tfd/detail_recibo_tfd.html'
    allowed_roles=['regulacao','secretario','coordenador']


    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        recibo_tfd= ReciboTFD.objects.select_related('paciente').get(id=self.kwargs['pk'])
        
        context['recibo_tfd']=recibo_tfd
        context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd','codigosia').filter(recibo_tfd__id=recibo_tfd.id)
        
        return context

class ReciboTFDDeleteView(HasRoleMixin,SuccessMessageMixin, DeleteView):

    model=ReciboTFD
    success_url=reverse_lazy('tfds:list-recibo_tfd')
    success_message='Registro excluido com sucesso '
    allowed_roles=['coordenador']


    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)

has_role_decorator(['regulacao','coordenador','secretario'])  
def reciboTFD_pdf(request,id):
    recibo_pdf=get_object_or_404(ReciboTFD,id=id)
    context={}

    context['recibo_tfd']= ReciboTFD.objects.select_related('paciente').get(id=recibo_pdf.id)
    context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd').filter(recibo_tfd__id=context['recibo_tfd'].id)

    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('recibo_tfd/pdf_recibo_tfd.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)


    return response