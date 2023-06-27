from django.urls import path

from usuarios import views

app_name='usuarios'
 
urlpatterns = [
        path('create/usuario',views.UsuarioCreateView.as_view(),name='add-usuario'),
        path('update/<int:pk>/usuario',views.UsuarioUpdateView.as_view(),name='edit-usuario'),
        path('detail/<int:pk>/usuario',views.UsuarioDetailView.as_view(),name='detail-usuario'),
        path('list/usuarios',views.UsuarioListView.as_view(),name='list-usuario'),


]
