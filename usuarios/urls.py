from django.contrib.auth import views as auth_views
from django.urls import path

from usuarios import views

app_name='usuarios'
 
urlpatterns = [
        path('create/usuario',views.UsuarioCreateView.as_view(),name='add-usuario'),
        path('update/<int:pk>/usuario',views.UsuarioUpdateView.as_view(),name='edit-usuario'),
        path('detail/<int:pk>/usuario',views.UsuarioDetailView.as_view(),name='detail-usuario'),
        path('list/usuarios',views.UsuarioListView.as_view(),name='list-usuario'),


        path('autenticacao/login', auth_views.LoginView.as_view(),name='login_usuario'),
        path('autenticacao/logout', auth_views.LogoutView.as_view(),name='deslogar_usuario'),


]
