from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,UpdateView
from rolepermissions.decorators import has_role_decorator
from django.contrib.messages.views import SuccessMessageMixin
from transportes.forms.destino_viagem_form import DestinoViagemForm
from transportes.models import DestinoViagem
from django.utils.decorators import method_decorator
from dal import autocomplete
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['regulacao','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DestinoViagemCreateView(SuccessMessageMixin,CreateView):
    model=DestinoViagem
    form_class=DestinoViagemForm
    success_url=reverse_lazy('transportes:list-destino')
    template_name='destino_viagem/form_destino_viagem.html' 
    context_object_name='form'
    success_message='Cadastro realizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class  DestinoViagemteUpdateView(SuccessMessageMixin,UpdateView):
    model=DestinoViagem
    form_class=DestinoViagemForm
    success_url=reverse_lazy('transportes:list-destino')
    template_name='destino_viagem/form_destino_viagem.html' 
    context_object_name='form'
    success_message='Dados atualizado com sucesso'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['regulacao','secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class DestinoViagemListView(ListView):

    model=DestinoViagem
    template_name='destino_viagem/list_destino_viagem.html'
    context_object_name='destino_viagens'
    paginate_by=20

    def get_queryset(self):
        qs=super(DestinoViagemListView,self).get_queryset()
        buscar=self.request.GET.get('buscar',None)

        if buscar:
            buscar=buscar.rstrip()
            queryset=qs.filter(nome__unaccent__icontains=buscar).order_by('nome')
            return queryset 

        qs=qs.all().order_by('nome')                                          
        
        return qs

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
class DestinoViagemAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return DestinoViagem.objects.none()
        
        qs = DestinoViagem.objects.all()
        
        if self.q:
            self.q=self.q.rstrip()
            qs = qs.filter(nome__unaccent__icontains=self.q)

        return qs

