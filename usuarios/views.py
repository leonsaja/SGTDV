from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from usuarios.forms import CadastroUsuarioForm, EditarUsuarioForm
from rolepermissions.roles import assign_role
from rolepermissions.mixins import HasRoleMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rolepermissions.decorators import has_role_decorator

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class UsuarioCreateView(SuccessMessageMixin,CreateView):
            
    User=get_user_model()
    model=User
    form_class=CadastroUsuarioForm
    template_name='usuario/add_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Cadastro realizado com sucesso'
  
    def form_valid(self, form):
        user=form.save()
        if user.perfil =='1':
            assign_role(user,'acs')
        elif user.perfil == '2':
            assign_role(user,'coordenador')
        elif user.perfil =='3':
            assign_role(user,'digitador')
        elif user.perfil== '4':
            assign_role(user,'recepcao')
        elif user.perfil=='5':
            assign_role(user,'secretario')
        elif user.perfil =='6':
            assign_role(user,'regulacao')
        elif user.perfil =='7':
            assign_role(user,'tfd')
        return super().form_valid(form)
 
@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class UsuarioUpdateView(SuccessMessageMixin,UpdateView):
    
    User=get_user_model()
    model=User
    form_class=EditarUsuarioForm
    template_name='usuario/edit_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Dados atualizado com sucesso'
    #allowed_roles = ['acs','secretario','regulacao',]

    def form_valid(self, form):
        user=form.save()
    
        if user.perfil =='1':
            assign_role(user,'acs')
        elif user.perfil == '2':
            assign_role(user,'coordenador')
        elif user.perfil =='3':
            assign_role(user,'digitador')
        elif user.perfil== '4':
            assign_role(user,'recepcao')
        elif user.perfil=='5':
            assign_role(user,'secretario')
        elif user.perfil =='6':
            assign_role(user,'regulacao')
        elif user.perfil =='7':
            assign_role(user,'tfd')
        return super().form_valid(form)

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class UsuarioListView(ListView):
   
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=10
    queryset=User.objects.filter(is_staff=False).filter(is_active=True)
    ordering='-created_at'

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class UsuarioSearchListView(ListView):
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(UsuarioSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
        desativado=self.request.GET.get('check',None)
       
        if search_nome_cpf:
            qs=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf)).order_by('-nome_completo')
        
        if data:
             qs=qs.filter(dt_nascimento__iexact=data).filter(is_staff=False).order_by('-nome_completo')
         
        if desativado:
             qs=qs.filter(is_active=False).filter(is_staff=False).order_by('-nome_completo')
   
        return qs

@method_decorator(login_required(login_url='usuarios:login_usuario'), name='dispatch')
@method_decorator(has_role_decorator(['secretario','coordenador'], redirect_url=reverse_lazy('usuarios:acesso_negado')), name='dispatch')
class UsuarioDetailView(DetailView):
    User=get_user_model()
    model=User
    template_name='usuario/detail_usuario.html'
    context_object_name='usuario'

class PasswordChange(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):
     form_class = PasswordChangeForm
     template_name='registration/alterar_senha.html'
     success_url=reverse_lazy('core:home')
     success_message='Senha alterado com sucesso'
     
class AcessoNegadoView(LoginRequiredMixin,TemplateView):
  
    template_name = 'usuario/acesso_negado.html'
    
"""def custom_lockout(request, credentials=None, *args, **kwargs):
    username = credentials.get('username') if credentials else ''
    # monta a URL com o parâmetro
    url = reverse('usuarios:login_bloqueado') + f'?username={username}'
    return HttpResponseRedirect(url)


def usuario_bloqueado(request):
    
    # Você pode capturar informações do request se quiser:
    username = request.GET.get('username', '')
    ip = request.META.get('REMOTE_ADDR')

    return render(request, 'registration/login_bloqueado.html', {
        'username': username,
        'ip': ip,
    })
"""