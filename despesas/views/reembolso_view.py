from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q
from io import BytesIO
from django.contrib.messages.views import SuccessMessageMixin
from despesas.forms.reembolso_form import ReembolFormSet,ReembolsoPrincipalForm,ReembolsoStatusForm
from despesas.models import Diaria, Reembolso,ReembolsoPrincipal
from django.contrib.messages import constants
from django.contrib import messages
from django.utils.decorators import method_decorator
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin
from django.contrib.auth.decorators import login_required

@login_required
@has_role_decorator(['digitador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def reembolso_create(request,id):
    diaria=get_object_or_404(Diaria,id=id)
    
    if not diaria:
        return Http404()
    try:
        reembolso = ReembolsoPrincipal.objects.get(diaria=diaria)
    except ReembolsoPrincipal.DoesNotExist:
        reembolso = ReembolsoPrincipal(diaria=diaria)
        
    if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=reembolso,prefix='reembolso')
        form=ReembolsoPrincipalForm(request.POST or None,instance=reembolso,prefix='reembolso_diaria')

        if formset.is_valid() and form.is_valid():
            form=form.save(commit=False)
            form.criado_por=request.user.nome_completo
            form.save()
            formset.diaria=form
            formset.save()
            messages.add_message(request,constants.SUCCESS,'cadastro realizado com sucesso')
            return redirect('despesas:list-reembolso')

    formset=ReembolFormSet(request.POST or None,instance=reembolso,prefix='reembolso')
    form=ReembolsoPrincipalForm(request.POST or None,instance=reembolso,prefix='reembolso_diaria')
    
    return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset,'form':form})

@login_required
@has_role_decorator(['digitador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def reembolso_update(request, id):
   diaria=get_object_or_404(Diaria,id=id)
    
   if not diaria:
        return Http404()
   try:
        reembolso = ReembolsoPrincipal.objects.get(diaria=diaria)
   except ReembolsoPrincipal.DoesNotExist:
        reembolso = ReembolsoPrincipal(diaria=diaria)
        
   if request.method == 'POST':
        formset=ReembolFormSet(request.POST,instance=reembolso,prefix='reembolso')
        form=ReembolsoPrincipalForm(request.POST or None,instance=reembolso,prefix='reembolso_diaria')

        if formset.is_valid() and form.is_valid():
            form=form.save(commit=False)
            form.alterado_por=request.user.nome_completo
            form.save()
            formset.diaria=form
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('despesas:list-reembolso')
        

   formset=ReembolFormSet(request.POST or None,instance=reembolso,prefix='reembolso')
   form=ReembolsoPrincipalForm(request.POST or None,instance=reembolso,prefix='reembolso_diaria')

   return render(request, 'reembolso/form_reembolso.html', {'diaria': diaria,'formset':formset,'form':form})

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')  
class ReembolsoListView(ListView):
   
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   queryset=Diaria.objects.select_related('profissional').filter(reembolso=1)
   ordering='-created_at'
   paginate_by=10
   
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')  
class ReembolsoSearchListView(ListView):
   model=Diaria
   template_name='reembolso/list_reembolso.html'
   context_object_name='diarias'
   paginate_by=10

   def get_queryset(self, *args, **kwargs):
        qs = super(ReembolsoSearchListView,self).get_queryset(*args, **kwargs)
        buscar=self.request.GET.get('buscar',None)
        data=self.request.GET.get('data',None)
        
        if buscar:
            qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(Q(profissional__nome_completo__icontains=buscar)| Q(profissional__cpf__icontains=buscar)).order_by('-created_at')
        
        if data:
             qs=qs.select_related('profissional')\
                .filter(reembolso=1).filter(data_diaria__iexact=data).order_by('-created_at')
            
        return qs 

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ReembolsoStatusUpdateView(SuccessMessageMixin, UpdateView):
    
   model=ReembolsoPrincipal
   form_class=ReembolsoStatusForm 
   template_name='reembolso/detail_reembolso.html'
   success_url=reverse_lazy('despesas:list-reembolso')
   success_message='Operação realizado com sucesso'

   def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aprovado_por = self.request.user.nome_completo
        self.object.save()
        return  super().form_valid(form)
    

@method_decorator(has_role_decorator(['digitador','coordenador','secretario'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')  
class ReembolsoDetailView(DetailView):
    model=Diaria
    template_name='reembolso/detail_reembolso.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        diaria=Diaria.objects.select_related('profissional').get(id=self.kwargs['pk'])
        context['diaria']=diaria
        try:
            reembolso = ReembolsoPrincipal.objects.select_related('diaria').get(diaria=diaria)
        except ReembolsoPrincipal.DoesNotExist:
            reembolso = ReembolsoPrincipal(diaria=diaria)
        context['reem_principal']=reembolso
        context['reembolsos'] =Reembolso.objects.select_related('reembolso_principal').filter(reembolso_principal__diaria__id=diaria.id)
        context['form']=ReembolsoStatusForm(self.request.POST or None,instance=reembolso)

        return context

@login_required
@has_role_decorator(['digitador','coordenador','secretario'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def reembolso_pdf(request,id):
    context={}
    diaria=get_object_or_404(Diaria,id=id)
    User=get_user_model()
   
    context['diaria']=diaria
    try:
        reembolso = ReembolsoPrincipal.objects.select_related('diaria').get(diaria=diaria)
    except ReembolsoPrincipal.DoesNotExist:
        reembolso = ReembolsoPrincipal(diaria=diaria)
        
    context['reem_principal']=reembolso
    context['reembolsos'] =Reembolso.objects.select_related('reembolso_principal').filter(reembolso_principal__diaria__id=diaria.id)
    context['profissional']=User.objects.filter(is_active=True).filter(perfil='5').first()
    
    buffer = BytesIO()
    html_string = render_to_string('reembolso/pdf_reembolso.html', context)
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Reembolso_{diaria.profissional.profis()}_{diaria.data_diaria.strftime("%d/%m/%Y")}.pdf"'

    return response
    
   