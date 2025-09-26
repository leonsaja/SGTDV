from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from .forms import CustomAuthenticationForm

from usuarios import views

app_name='usuarios'
 
urlpatterns = [
    
        path('create/usuario',views.UsuarioCreateView.as_view(),name='add-usuario'),
        path('update/<int:pk>/usuario',views.UsuarioUpdateView.as_view(),name='edit-usuario'),
        path('detail/<int:pk>/usuario',views.UsuarioDetailView.as_view(),name='detail-usuario'),
        path('list/usuarios',views.UsuarioListView.as_view(),name='list-usuario'),
        path('search/usuario',views.UsuarioSearchListView.as_view(),name='search-usuario'),
        #path('login_bloqueado',views.usuario_bloqueado, name='login_bloqueado'),

        path('autenticacao/login', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm,redirect_authenticated_user = True),name='login_usuario'),
        path('autenticacao/logout', auth_views.LogoutView.as_view(),name='deslogar_usuario'),
        path('alterar_senha/usuario', views.PasswordChange.as_view(), name='alterar_senha'),
        path('acesso-negado', views.AcessoNegadoView.as_view(), name='acesso_negado'),

        path('resetar_senha',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('usuarios:password_reset_done')),name='resetar_senha'),
        path('resetar_senha/sucesso',auth_views.PasswordResetCompleteView.as_view(), name='resetar_senha_sucesso'),
        path('resetar_senha/<str:uidb64>/<str:token>',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('usuarios:resetar_senha_sucesso')),name='password_reset_confirm'),
        path('resetar_senha/feito',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

]
