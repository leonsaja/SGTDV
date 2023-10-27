from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from usuarios.forms import CadastroUsuarioForm, EditarUsuarioForm


class UsuarioCreateView(SuccessMessageMixin,CreateView):
    User=get_user_model()
    model=User
    form_class=CadastroUsuarioForm
    template_name='usuario/add_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Cadastro realizado com sucesso'

class UsuarioUpdateView(SuccessMessageMixin,UpdateView):
    
    User=get_user_model()
    model=User
    form_class=EditarUsuarioForm
    template_name='usuario/edit_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')
    success_message='Dados atualizado com sucesso'

class UsuarioListView(ListView):
   
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=10
    queryset=User.objects.filter(is_staff=False).filter(is_active=True)
    ordering='-created_at'
        
class UsuarioSearchListView(ListView):
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    paginate_by=1

    
    def get_queryset(self, *args, **kwargs):
        qs = super(UsuarioSearchListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)
        desativado=self.request.GET.get('check',None)
        print('user', self.request.GET)

        if search_nome_cpf and data:
            qs=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(dt_nascimento__iexact=data).order_by('-nome_completo')
           
        elif search_nome_cpf and desativado:
             qs=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(is_active=False).filter(is_staff=False).order_by('-nome_completo')

        elif search_nome_cpf:
            qs=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf)).filter(is_staff=False).order_by('nome_completo')
        
        elif data:
             qs=qs.filter(dt_nascimento__iexact=data).filter(is_staff=False).order_by('nome_completo')
        
        elif desativado:
              print('teste')
              qs=qs.filter(is_active=False).filter(is_staff=False).order_by('nome_completo')
       
        return qs

class UsuarioDetailView(DetailView):
    User=get_user_model()
    model=User
    template_name='usuario/detail_usuario.html'
    context_object_name='usuario'