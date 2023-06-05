from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from usuarios.forms import CadastroUsuarioForm, EditarUsuarioForm
from usuarios.models import Usuario


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

class ListaUsuarioView(ListView):
    User=get_user_model()
    model=User
    template_name='usuario/list_usuarios.html'
    context_object_name='usuarios'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
       
        qs = qs.filter(is_staff=False)
        return qs
    

class DetailUsuarioView(DetailView):
    User=get_user_model()
    model=User
    template_name='usuario/detail_usuario.html'
    context_object_name='usuario'