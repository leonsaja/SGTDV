from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.db.models import ProtectedError
from ..forms.carro_form import CarroForm
from ..models import Carro
from django.contrib.messages.views import SuccessMessageMixin
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.decorators import has_role_decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CarroCreateView(SuccessMessageMixin,CreateView):
    model=Carro
    form_class=CarroForm
    template_name='carro/form_carro.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-carro')
    success_message='Cadastro realizado com sucesso'
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['recepcao','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class CarroUpdateView(SuccessMessageMixin,UpdateView):  

    model=Carro
    form_class=CarroForm
    template_name='carro/form_carro.html'
    context_object_name='form'
    success_url=reverse_lazy('transportes:list-carro')
    success_message='Dados atualizado com sucesso'
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario','regulacao','recepcao','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class ListCarroView(ListView):
    model=Carro
    template_name='carro/list_carros.html'
    context_object_name='carros'
    paginate_by=10  

    def get_queryset(self):
        qs=super(ListCarroView,self).get_queryset()
        #buscar=self.request.GET.get('buscar',None)

        """if buscar:
            queryset=qs.filter(nome__icontains=buscar).order_by('-nome')
            return queryset """

        qs=qs.filter(status='1').order_by('nome')                                          
        
        return qs
    
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador','secretario','regulacao','recepcao','digitador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DetailCarraView(DetailView):
    model=Carro
    template_name='carro/detail_carro.html'
    context_object_name='carro'

@login_required
@has_role_decorator(['coordenador'],redirect_url=reverse_lazy('usuarios:acesso_negado'))
def carroDelete(request, id):

    carro=get_object_or_404(Carro,id=id)
    
    try:
        carro.delete()
        messages.add_message(request,constants.SUCCESS, "Registro excluido com sucesso")
    except ProtectedError:
        messages.add_message(request,constants.ERROR,"Infelizmente não foi possível, pois existe  uma ou mais referências e não pode ser excluído.")
    finally:
        return redirect('transportes:list-carro')

