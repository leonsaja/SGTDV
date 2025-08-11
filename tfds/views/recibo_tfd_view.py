from django.db.models import  Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
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

@has_role_decorator(['regulacao'])
def reciboTFD_create(request):
    tfd = ReciboTFD()

    if request.method == 'POST':
        form = ReciboTFDForm(request.POST, instance=tfd, prefix='recibo')
        formset = ProcedimentoSet(request.POST, instance=tfd, prefix='procedimento')

        if form.is_valid() and formset.is_valid():
            # 1. Salva a instância principal do ReciboTFD (o "recibo pai")
            #    Ela agora tem um ID
            recibo_instance = form.save(commit=False)
            recibo_instance.criado_por = request.user.nome_completo
            recibo_instance.save()

            # 2. Salva o formset, associando os procedimentos ao recibo
            formset.instance = recibo_instance
            formset.save()

            # 3. Recalcula o total agora que os procedimentos já foram salvos
            recibo_instance.total_gasto = recibo_instance.calcular_total_gasto()
            recibo_instance.save(update_fields=['total_gasto'])

            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return redirect('tfds:list-recibo_tfd')

    # GET request or form is invalid
    else:
        form = ReciboTFDForm(instance=tfd, prefix='recibo')
        formset = ProcedimentoSet(instance=tfd, prefix='procedimento')

    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form, 'formset': formset})
@has_role_decorator(['regulacao'])  
def reciboTFD_update(request,id):
    recibo_tfd=get_object_or_404(ReciboTFD, pk=id)

    if request.method =='POST':
        form=ReciboTFDForm(request.POST, instance=recibo_tfd,prefix='recibo')
        formset=ProcedimentoSet(request.POST, instance=recibo_tfd,prefix='procedimento')
        
        if form.is_valid() and formset.is_valid():
            # 1. Salva a instância principal do ReciboTFD, mas sem enviar ao banco ainda.
            recibo_instance = form.save(commit=False)
            recibo_instance.criado_por = request.user.nome_completo
            
            # 2. Salva o ReciboTFD no banco de dados.
            recibo_instance.save()
            
            # 3. Salva o formset. Isso adiciona/atualiza/deleta os ProcedimentoSia.
            formset.save()
            
            # 4. **Recalcula o total gasto.**
            #    Agora que o formset já foi salvo, o método calcular_total_gasto()
            #    encontrará os dados corretos no banco.
            recibo_instance.total_gasto = recibo_instance.calcular_total_gasto()
            recibo_instance.save(update_fields=['total_gasto']) # Salva apenas o campo atualizado

            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('tfds:list-recibo_tfd')
        
    form=ReciboTFDForm(instance=recibo_tfd,prefix='recibo')
    formset=ProcedimentoSet(instance=recibo_tfd,prefix='procedimento')
    return render(request, 'recibo_tfd/form_recibo_tfd.html', {'form': form,'formset':formset,'recibo_tfd':recibo_tfd})
@has_role_decorator(['secretario'])  
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

    form=ReciboTFDStatusForm(request.POST or None, instance=recibo_tfd,prefix='recibo')
    
    return render(request, 'recibo_tfd/detail_recibo_tfd.html', {'form': form,'recibo_tfd':recibo_tfd})

class ReciboTFDListView(HasRoleMixin,ListView):

    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10
    allowed_roles=['regulacao','secretario','coordenador']

    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('paciente','especialidade','acompanhante').order_by('-created_at')
        return qs
    
class ReciboTFDSearchListView(HasRoleMixin,ListView):
   
    model=ReciboTFD
    template_name='recibo_tfd/list_recibos_tfds.html'
    context_object_name='recibos_tfds'
    paginate_by=10
    allowed_roles=['regulacao','secretario','coordenador']

    
    def get_queryset(self, *args, **kwargs):
        qs = super(ReciboTFDSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None).rstrip()
        data=self.request.GET.get('data',None)
      
        if search_nome_cpf:
            qs=qs.select_related('paciente','especialidade','acompanhante').filter(Q(paciente__nome_completo__icontains=search_nome_cpf)| Q(paciente__cpf__icontains=search_nome_cpf))\
            .order_by('-data')
           
        if data:
             qs=qs.select_related('paciente','especialidade','acompanhante').filter(data__iexact=data).order_by('-created_at')
        
        return qs

class ReciboTFDDetailView(HasRoleMixin,DetailView):

    model=ReciboTFD
    template_name='recibo_tfd/detail_recibo_tfd.html'
    allowed_roles=['regulacao','secretario','coordenador']
    
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        recibo_tfd= ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').get(id=self.kwargs['pk'])
        context['recibo_tfd']=recibo_tfd
        context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd','codigosia').filter(recibo_tfd__id=recibo_tfd.id)
        context['form']=ReciboTFDStatusForm(self.request.POST or None, instance=recibo_tfd,prefix='recibo')
        return context

class ReciboTFDDeleteView(HasRoleMixin,SuccessMessageMixin, DeleteView):

    model=ReciboTFD
    success_url=reverse_lazy('tfds:list-recibo_tfd')
    success_message='Registro excluido com sucesso '
    allowed_roles=['coordenador']


    def get(self, request, *args, **kwargs):
        return self.post().get(request, *args, **kwargs)

@has_role_decorator(['regulacao','coordenador','secretario'])  
def reciboTFD_pdf(request,id):
    recibo_pdf=get_object_or_404(ReciboTFD,id=id)
    context={}

    context['recibo_tfd']= ReciboTFD.objects.select_related('paciente','especialidade','acompanhante').get(id=recibo_pdf.id)
    context['procedimentos']=ProcedimentoSia.objects.select_related('recibo_tfd','codigosia').filter(recibo_tfd__id=context['recibo_tfd'].id)
   
    User=get_user_model()
    context['profissional']=User.objects.filter(is_active=True).filter(perfil='5').first()
    context['n_tfd']=f'{context["recibo_tfd"].id}/{datetime.date.today().year}'
    response = HttpResponse(content_type='application/pdf')
    html_string = render_to_string('recibo_tfd/pdf_recibo_tfd.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)


    return response