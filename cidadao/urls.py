from django.urls import path

from cidadao import views as view_cidadao

app_name='cidadao'

urlpatterns = [
    path('create/cidadao', view_cidadao.cidadao_create, name='add-cidadao' ),
    path('update/<int:id>/cidadao', view_cidadao.cidadao_update , name='edit-cidadao' ),
    path('list/cidadao', view_cidadao.CidadaoListView.as_view(), name='list-cidadao' ),
    path('search/cidadao', view_cidadao.CidadaoSearchListView.as_view(), name='search-cidadao'),
    path('detail/<int:pk>/cidadao', view_cidadao.CidadaoDetailView.as_view(), name='detail-cidadao' ),
    path('delete/<int:id>/cidadao', view_cidadao.cidadao_delete , name='del-cidadao' ),
    #path('importacao dados/cidadao', view_cidadao.ImportDadosView.as_view() , name='importar-dados-cidadao' )""
    
    
    
]