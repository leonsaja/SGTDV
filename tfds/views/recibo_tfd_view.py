from django.db.models import  Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView,CreateView,ListView
from tfds.forms.form_recibo_tfd import ReciboTFDForm,ReciboTFDStatusForm
from tfds.forms.form_procedimento import ProcedimentoSet
from tfds.models import  ReciboTFD,ProcedimentoSia
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from io import BytesIO
from django.utils.decorators import method_decorator

@method_decorator(has_role_decorator(['tfd'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDCreateView(SuccessMessageMixin,CreateView):
    
    model=ReciboTFD
    form_class=ReciboTFDForm
    template_name='recibo_tfd/form_recibo_tfd.html'
    success_url=reverse_lazy('tfds:list-recibo_tfd')
    success_message='Recibo cadastrado com sucesso'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = 'recibo'
        return kwargs
  
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset']=ProcedimentoSet(self.request.POST, instance=self.object, prefix='procedimento')
        else:
            context['formset']=ProcedimentoSet(instance=self.object, prefix='procedimento')

        return context
    
    def form_valid(self, form):
        
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user.nome_completo
            self.object.save()
            formset.instance = self.object  # Garante que o formset esteja ligado ao novo objeto
            formset.save()
            self.object.total_gasto = self.object.calcular_total_gasto()
            self.object.save(update_fields=['total_gasto'])
            return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

@method_decorator(has_role_decorator(['tfd'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDUpdateView(SuccessMessageMixin,UpdateView):
    model=ReciboTFD
    form_class=ReciboTFDForm
    template_name='recibo_tfd/form_recibo_tfd.html'
    success_url=reverse_lazy('tfds:list-recibo_tfd')
    allowed_roles=['regulacao']
    success_message='Recibo alterado com sucesso'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = 'recibo'
        return kwargs
  
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset']=ProcedimentoSet(self.request.POST, instance=self.object, prefix='procedimento')
        else:
            context['formset']=ProcedimentoSet(instance=self.object, prefix='procedimento')
        return context
    
    def form_valid(self, form):
        
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.alterado_por = self.request.user.nome_completo
            self.object.save()
            formset.instance = self.object  # Garante que o formset esteja ligado ao novo objeto
            formset.save()
            self.object.total_gasto = self.object.calcular_total_gasto()
            self.object.save(update_fields=['total_gasto'])
            return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

@has_role_decorator(['regulacao'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def reciboStatusUpdate(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=ReciboTFDStatusForm(request.POST, instance=recibo_tfd,prefix='recibo')
        if form.is_valid():
           form=form.save(commit=False)
           form.aprovado_por=request.user.nome_completo
           form.save()
           messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
           return redirect('tfds:list-recibo_tfd')

    else:
        form=ReciboTFDStatusForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    
    return render(request, 'recibo_tfd/detail_recibo_tfd.html', {'form': form,'recibo_tfd':recibo_tfd})

@method_decorator(has_role_decorator(['tfd','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDListView(ListView):

    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    ordering='-created_at'
    paginate_by=10

@method_decorator(has_role_decorator(['tfd','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDSearchListView(ListView):
   
    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None).rstrip()
        data=self.request.GET.get('data',None)
        
        qs=qs.select_related('paciente','especialidade','acompanhante').order_by('-paciente__nome_completo')
        
        if search_nome_cpf:
            qs=qs.filter(Q(paciente__nome_completo__unaccent__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))
           
        if data:
             qs=qs.filter(data__iexact=data)
        
        return qs

@method_decorator(has_role_decorator(['tfd','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDDetailView(DetailView):

    model=ReciboTFD
    template_name='recibo_tfd/detail_recibo_tfd.html'
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        recibo_tfd= ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').get(id=self.kwargs['pk'])
        context['recibo_tfd']=recibo_tfd
        context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd','codigosia').filter(recibo_tfd__id=recibo_tfd.id)
        context['form']=ReciboTFDStatusForm(self.request.POST or None, instance=recibo_tfd,prefix='recibo')
        return context

@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')   
class ReciboTFDDeleteView(SuccessMessageMixin, DeleteView):

    model=ReciboTFD
    success_url=reverse_lazy('tfds:list-recibo_tfd')
    success_message='Registro excluido com sucesso '

    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)

@has_role_decorator(['tfd','coordenador','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def reciboTFD_pdf(request,id):
    recibo_pdf=get_object_or_404(ReciboTFD,id=id)
    context={}

    context['recibo_tfd']= ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').get(id=recibo_pdf.id)
    context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd','codigosia').filter(recibo_tfd__id=context['recibo_tfd'].id)
   
    User=get_user_model()
    context['profissional']=User.objects.filter(is_active=True).filter(perfil='5').first()
    context['n_tfd']=f'{context["recibo_tfd"].id}/{datetime.date.today().year}'
    
    buffer = BytesIO()
    html_string = render_to_string('recibo_tfd/pdf_recibo_tfd.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Recibo_TFD_{recibo_pdf.paciente.nome_cidadao()}_{recibo_pdf.data.strftime("%d/%m/%Y")}.pdf"'


    return response