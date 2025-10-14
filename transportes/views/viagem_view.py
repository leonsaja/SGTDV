from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView,UpdateView,CreateView
from weasyprint import HTML
from ..forms.viagem_form import PassageiroViagemSet, ViagemForm
from ..models import Viagem
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from transportes.models import PassageiroViagem
from django.urls import reverse_lazy
from io import BytesIO
from django.db.models import  Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ViagemCreateView(SuccessMessageMixin,CreateView):
    model=Viagem
    form_class=ViagemForm
    template_name='viagem/form_viagem.html'
    success_url=reverse_lazy('transportes:list-viagem')
    success_message='Viagem cadastrada com sucesso'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PassageiroViagemSet(self.request.POST, prefix='passageiro')
        else:
            context['formset'] = PassageiroViagemSet(prefix='passageiro')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user.nome_completo
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ViagemUpdateView(SuccessMessageMixin, UpdateView):
    model = Viagem
    form_class = ViagemForm
    template_name = 'viagem/form_viagem.html'
    success_url = reverse_lazy('transportes:list-viagem')
    success_message='Viagem atualizada com sucesso'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PassageiroViagemSet(self.request.POST, instance=self.object, prefix='passageiro')
        else:
            context['formset'] = PassageiroViagemSet(instance=self.object, prefix='passageiro')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.alterado_por = self.request.user.nome_completo
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['acs','digitador','recepcao','regulacao','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ViagemListView(ListView): 
    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10

    def get_queryset(self, *args, **kwargs):
        qs =super(ViagemListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('carro','motorista').filter(status='1').order_by('-data_viagem')
        return qs
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['acs','digitador','recepcao','regulacao','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ViagemSearchListView(ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10


    def get_queryset(self, *args, **kwargs):
        qs = super(ViagemSearchListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('motorista','carro').all()

        destino_viagem=self.request.GET.get('destino_viagem',None)
        placa_carro=self.request.GET.get('placa_carro',None)
        data=self.request.GET.get('data',None)
        status=self.request.GET.get('status',None)
        

        if destino_viagem:
            qs=qs.filter(destino_viagem__icontains=destino_viagem).order_by('-data_viagem')
        if placa_carro:
            qs=qs.filter(carro__placa__icontains=placa_carro).order_by('-data_viagem')       
        if data :
             qs=qs.filter(data_viagem__iexact=data).order_by('-data_viagem')
        if status:
            qs=qs.filter(status=status).order_by('-data_viagem')
        return qs

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['acs','digitador','recepcao','regulacao','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DetailViagemView(SuccessMessageMixin,DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viagem = Viagem.objects.select_related('motorista','carro').get(id=self.kwargs['pk']) 
        context['viagem']=viagem
        return context

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ViagemDeleteView(SuccessMessageMixin,DeleteView):

    model=Viagem
    success_url=reverse_lazy('transportes:list-viagem')
    success_message='Registro excluido com sucesso'
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

@login_required
@has_role_decorator(['recepcao','digitador','regulacao'])
def viagemPdf(request,id):
    context={}

    viagem=get_object_or_404(Viagem,id=id)
    total=0
    for passageiro in viagem.passageiros_viagens.all():
        if passageiro.paciente:
            total+=1
        if passageiro.acompanhante:
            total+=1
    capacidade=viagem.carro.qta_passageiro
    
    micro_onibus=False
    
    if capacidade>22:
         micro_onibus=True
         
    
    carro_lotado=False
    if total>=capacidade:
        carro_lotado=True
        
    context['carro_lotado']=carro_lotado
    context['viagem']=viagem
    context['total']=total
    context['cap']=capacidade

    context['micro_onibus']=micro_onibus
    capacidade=range(capacidade)
    context['capacidade']=capacidade
   
    if micro_onibus:
       html_string = render_to_string('viagem/pdf_viagem_micro.html',context)
    
    else:
        html_string = render_to_string('viagem/pdf_viagem.html',context)
    
    buffer = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Viagem_{viagem.destino_viagem}_{viagem.data_viagem.strftime("%d/%m/%Y")}.pdf"'

    return response

@login_required
class PacienteViagemSearchView(HasRoleMixin,ListView):
   
    model = PassageiroViagem
    template_name = 'buscar_paciente_viagem.html'
    paginate_by = 10
    pk_url_kwarg = 'id'
    allowed_roles=['recepcao','regulacao','secretario','coordenador','acs']

    def get_queryset(self):
        buscar = self.request.GET.get('buscar', None)
        queryset = PassageiroViagem.objects.select_related('paciente').all()

        if buscar:
            buscar=buscar.rstrip()
            queryset = queryset.filter(
                Q(paciente__nome_completo__unaccent__icontainss=buscar) | Q(paciente__cpf__icontains=buscar)
            )
            
        return queryset