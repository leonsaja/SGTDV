from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from usuarios.forms import CadastroUsuarioForm, EditarUsuarioForm
from rolepermissions.roles import assign_role
from rolepermissions.mixins import HasRoleMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


class UsuarioCreateView(HasRoleMixin,SuccessMessageMixin,CreateView):
            
    User=get_user_model()
    model=User
    form_class=CadastroUsuarioForm
    template_name='usuario/add_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Cadastro realizado com sucesso'
    allowed_roles = ['secretario','coordenador']
    

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
        return super().form_valid(form)
    
class UsuarioUpdateView(HasRoleMixin,SuccessMessageMixin,UpdateView):
    
    User=get_user_model()
    model=User
    form_class=EditarUsuarioForm
    template_name='usuario/edit_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Dados atualizado com sucesso'
    allowed_roles = ['acs','secretario','regulcao',]

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
        return super().form_valid(form)
    
class UsuarioListView(HasRoleMixin,ListView):
   
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=10
    queryset=User.objects.filter(is_staff=False).filter(is_active=True)
    ordering='-created_at'
    allowed_roles = ['secretario','coordenador']

class UsuarioSearchListView(HasRoleMixin,ListView):
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=10
    allowed_roles = ['secretario','coordenador']
    
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

class UsuarioDetailView(HasRoleMixin,DetailView):
    User=get_user_model()
    model=User
    template_name='usuario/detail_usuario.html'
    context_object_name='usuario'
    allowed_roles = ['secretario','coordenador']

class PasswordChange(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
     form_class = PasswordChangeForm
     template_name='registration/alterar_senha.html'
     success_url=reverse_lazy('core:home')
     success_message='Senha alterado com sucesso'