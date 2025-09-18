from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from weasyprint import HTML
from ..forms.viagem_form import PassageiroViagemSet, ViagemForm
from ..models import Viagem
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.messages import constants
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from transportes.models import PassageiroViagem

@has_role_decorator(['recepcao','regulacao'])
def viagemCreate(request):
    viagem=Viagem()
    if request.method == 'POST':

        form = ViagemForm(request.POST,instance=viagem,prefix='viagem' )
        formset=PassageiroViagemSet(request.POST,instance=viagem,prefix='passageiro')
        if form.is_valid() and formset.is_valid():
            
            viagem=form.save(commit=False)
            viagem.criado_por=request.user.nome_completo
            viagem.save()
            formset.instance=viagem
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Viagem cadastrada com sucesso')
           
            return redirect('transportes:list-viagem')

    form = ViagemForm(request.POST or None,instance=viagem,prefix='viagem')
    formset=PassageiroViagemSet(request.POST or None,instance=viagem,prefix='passageiro')
    
    return render(request, 'viagem/form_viagem.html', {'form': form,'formset':formset})

@has_role_decorator(['recepcao','regulacao'])
def viagemUpdate(request,id):

    viagem=Viagem.objects.get(id=id)

    if not viagem:
        not Http404()

    if request.method == 'POST':

        form = ViagemForm(request.POST,instance=viagem,prefix='viagem' )
        formset=PassageiroViagemSet(request.POST,instance=viagem,prefix='passageiro')
        if form.is_valid() and formset.is_valid(): 
            
            viagem=form.save(commit=False)
            viagem.alterado_por=request.user.nome_completo
            viagem.save()
            formset.instance=viagem
            formset.save()
            messages.add_message(request,constants.SUCCESS,'Dados atualizado com sucesso')
            return redirect('transportes:list-viagem')
         
         
        print(formset.errors)

    form = ViagemForm(request.POST or None,instance=viagem,prefix='viagem')
    formset=PassageiroViagemSet(request.POST or None,instance=viagem,prefix='passageiro')
    
    return render(request, 'viagem/form_viagem.html', {'form': form,'formset':formset})

class ViagemListView(HasRoleMixin,ListView): 
    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10
    allowed_roles=['acs','digitador','recepcao','regulacao','secretario','coordenador']

    def get_queryset(self, *args, **kwargs):
        qs =super(ViagemListView,self).get_queryset(*args, **kwargs)
        qs=qs.select_related('carro','motorista').filter(status='1').order_by('-data_viagem')
        return qs
    
class ViagemSearchListView(HasRoleMixin,ListView):

    model=Viagem
    template_name='viagem/list_viagens.html'
    context_object_name='viagens'
    paginate_by=10
    allowed_roles=['acs','digitador','recepcao','secretario','regulacao','coordenador']


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
    
class DetailViagemView(HasRoleMixin,SuccessMessageMixin,DetailView):
    model=Viagem
    template_name='viagem/detail_viagem.html'
    allowed_roles=['acs','digitador','secretario','recepcao','regulacao','coordenador']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viagem = Viagem.objects.select_related('motorista','carro').get(id=self.kwargs['pk']) 
        context['viagem']=viagem
        return context

class ViagemDeleteView(HasRoleMixin,SuccessMessageMixin,DeleteView):

    model=Viagem
    success_url=reverse_lazy('transportes:list-viagem')
    success_message='Registro excluido com sucesso'
    allowed_roles=['coordenador']
        
    def get(self, request,*args, **kwargs):
         return self.post(request, *args, **kwargs)

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
    response = HttpResponse(content_type='application/pdf')
    if micro_onibus:
       html_string = render_to_string('viagem/pdf_viagem_micro.html',context)
    
    else:
        html_string = render_to_string('viagem/pdf_viagem.html',context)
    
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

    return response


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