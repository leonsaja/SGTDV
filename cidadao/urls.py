from django.urls import path

from cidadao import views as view_cidadao

app_name='cidadao'

urlpatterns = [
    path('create/cidadao/', view_cidadao.cidadaoCreate, name='add-cidadao' ),
    path('update/<int:id>/cidadao/', view_cidadao.cidadaoUpdate , name='edit-cidadao' ),
    path('list/cidadao/', view_cidadao.CidadaoListView.as_view(), name='list-cidadao' ),
    path('detail/<int:pk>/cidadao/', view_cidadao.CidadaoDetailView.as_view(), name='detail-cidadao' ),
    path('delete/<int:id>/cidadao/', view_cidadao.cidadaoDelete , name='del-cidadao' )
    
]