from django.contrib import messages
from django.db.models import ProtectedError, Q
from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView,CreateView, UpdateView
from cidadao.forms.cidadao_form import CidadaoForm, EnderecoForm
from cidadao.models import Cidadao, Endereco
from especialidades.models import PacienteSia
from transportes.models import PassageiroViagem,RegistroTransporte
from django.contrib.messages import constants
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
import re
from django.utils.decorators import method_decorator

@method_decorator(has_role_decorator(['acs','recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CidadaoCreateView(SuccessMessageMixin,HasRoleMixin,CreateView):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html'
    success_url = reverse_lazy('cidadao:list-cidadao')
    success_message='Cadastro realizado com sucesso'
    allowed_roles=['acs','recepcao','regulacao']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['endereco'] = EnderecoForm(self.request.POST)
        else:
            context['endereco'] = EnderecoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['endereco']

        if form_endereco.is_valid():
            self.object = form.save()  
            form_endereco.instance.cidadao = self.object 
            form_endereco.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

@method_decorator(has_role_decorator(['acs','recepcao','regulacao'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CidadaoUpdateView(SuccessMessageMixin,UpdateView):
    model = Cidadao
    form_class = CidadaoForm
    template_name = 'cidadao/form_cidadao.html' 
    success_url = reverse_lazy('cidadao:list-cidadao')
    success_message='Dados atualizados com sucesso'

    def get_object(self, queryset=None):
        return get_object_or_404(Cidadao, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cidadao_instance = self.object
        try:
            endereco_instance = Endereco.objects.get(cidadao=cidadao_instance)
        except Endereco.DoesNotExist:
            endereco_instance = Endereco(cidadao=cidadao_instance) # Cria uma nova instância se não existir

        if self.request.POST:
            context['endereco'] = EnderecoForm(self.request.POST, instance=endereco_instance)
        else:
            context['endereco'] = EnderecoForm(instance=endereco_instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_endereco = context['endereco']

        if form_endereco.is_valid():
            self.object = form.save()
            form_endereco.instance.cidadao = self.object
            form_endereco.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)

@method_decorator(has_role_decorator(['acs','coordenador','regulacao','recepcao','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CidadaoDetailView(DetailView):
    model=Cidadao
    template_name='cidadao/detail_cidadao.html'

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['paciente']=Cidadao.objects.select_related('microarea').get(pk=self.kwargs['pk'])
        try:
            context['endereco']=Endereco.objects.select_related('cidadao').get(cidadao=context['paciente'])
        except Endereco.DoesNotExist:
            context['endereco']=Endereco(cidadao=context['paciente'])
        return context

@method_decorator(has_role_decorator(['acs','coordenador','regulacao','recepcao','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CidadaoListView(ListView):
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=15

@method_decorator(has_role_decorator(['acs','coordenador','regulacao','recepcao','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CidadaoSearchListView(ListView):
    
    model=Cidadao
    template_name='cidadao/list_cidadao.html'
    context_object_name='pacientes'
    paginate_by=10
   
    def get_queryset(self, *args, **kwargs):
        qs = super(CidadaoSearchListView,self).get_queryset(*args, **kwargs)

        search_nome_cpf_cns = self.request.GET.get('search_nome_cpf', '').strip()
        search_nome_mae = self.request.GET.get('search_nome_mae', '').strip()
        search_dt_nascimento = self.request.GET.get('search_dt_nascimento', None)
   
        if search_nome_cpf_cns:

            cpf_cns_limpo = re.sub(r'\D', '', search_nome_cpf_cns)
         
            if len(cpf_cns_limpo) == 11:
                qs = qs.filter(cpf=cpf_cns_limpo)
            elif len(cpf_cns_limpo) == 15:
                qs = qs.filter(cns=cpf_cns_limpo)
            else:
                qs = qs.filter(nome_completo__unaccent__icontains=search_nome_cpf_cns)

        if search_nome_mae:
            qs=qs.filter(nome_mae__icontains=search_nome_mae)
        
        if search_dt_nascimento:
            qs=qs.filter(dt_nascimento__iexact=search_dt_nascimento)

        return qs.select_related('microarea')

@has_role_decorator(['coordenador'],redirect_url='usuarios:acesso_negado')
def cidadao_delete(request,id):
    cidadao=get_object_or_404(Cidadao,id=id)

    try:
        cidadao.delete()
        messages.add_message(request, constants.SUCCESS ,"Registro excluido com sucesso")

    except ProtectedError:
        messages.add_message(request, constants.ERROR ,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('cidadao:list-cidadao')

class CidadaoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not self.request.user.is_authenticated:
            print('teste 1000')
            return Cidadao.objects.none()

        qs = Cidadao.objects.select_related('microarea').all()
        
        if self.q:
            cpf_cns_limpo = re.sub(r'\D', '', self.q)

            if len(cpf_cns_limpo) == 11:
                qs = qs.filter(cpf=cpf_cns_limpo)
            elif len(cpf_cns_limpo) == 15:
                qs = qs.filter(cns=cpf_cns_limpo)
            else:
                self.q=self.q.rstrip()
                qs = qs.filter(nome_completo__unaccent__icontains=self.q)
                
        return qs
    
@login_required
def cidadao_historico(request,id):
    paciente=get_object_or_404(Cidadao,id=id)
    context={}
    context['paciente']=paciente
    
   
    #Especialidade
    context['paciente_especialidades']=paciente.cidadao_especialidade.all       
    context['paciente_atendimentos']=PacienteSia.objects.filter(paciente__paciente=paciente).select_related('paciente', 'atendimento_paciente')
    context['paciente_recibos_tfds']=paciente.recibo_tfd_paciente.all
    context['paciente_recibos_tfds']=paciente.recibo_tfd_paciente.all
    context['paciente_viagens']=PassageiroViagem.objects.select_related('paciente','viagem').filter(paciente=paciente)
    context['registro_transportes']=RegistroTransporte.objects.select_related('paciente','carro').filter(paciente=paciente)
    return render(request,'cidadao/historico_cidadao.html',context)    
