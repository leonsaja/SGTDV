from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from usuarios.forms import CadastroUsuarioForm, EditarUsuarioForm


class UsuarioCreateView(CreateView):
    User=get_user_model()
    model=User
    form_class=CadastroUsuarioForm
    template_name='usuario/add_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')

class UsuarioUpdateView(UpdateView):
    User=get_user_model()
    model=User
    form_class=EditarUsuarioForm
    template_name='usuario/edit_usuario.html'
    context_object_name='form'
    success_url=reverse_lazy('usuarios:list-usuario')

class UsuarioListView(ListView):
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    
    def get_queryset(self, *args, **kwargs):
        qs = super(UsuarioListView,self).get_queryset(*args, **kwargs)
        
        search_nome_cpf=self.request.GET.get('search_nome_cpf',None)
        data=self.request.GET.get('data',None)

        if search_nome_cpf and data:
            queryset=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))\
                .filter(dt_nascimento__iexact=data)
            return queryset
        
        elif search_nome_cpf:
            queryset=qs.filter(Q(nome_completo__icontains=search_nome_cpf)| Q(cpf__icontains=search_nome_cpf))
            return queryset
        
        elif data:
             queryset=qs.filter(dt_nascimento__iexact=data).filter(is_staff=False)
             return queryset
        
        else:
            qs = qs.filter(is_staff=False)
            return qs
        
class UsuarioDetailView(DetailView):
    User=get_user_model()
    model=User
    template_name='usuario/detail_usuario.html'
    context_object_name='usuario'