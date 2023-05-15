
from django.urls import path

from .views import estabelecimento_view as est_view
from .views import microarea_view as micro_view

app_name='estabelecimentos'
urlpatterns = [

    #Estabelecimento
    path('create/estabelecimento/',est_view.EstabelecimentoCreateView.as_view(),name='add-estabelecimento'),                                                                                                                                                                                                                                                                  
    path('edit/<int:pk>/estabelecimento/',est_view.EstabelecimentoUpdateView.as_view(),name='edit-estabelecimento'),
    path('detail/<int:pk>/estabelecimento/',est_view.EstabelecimentoDetailView.as_view(),name='detail-estabelecimento'),
    path('list/estabelecimentos/',est_view.EstabelecimentoListView.as_view(),name='list-estabelecimento'),
    path('delete/<int:pk>/estabelecimento/',est_view.EstabelecimentoDeleteView.as_view(),name='del-estabelecimento'),

    #Micro Área
    path('create/microarea/',micro_view.MicroAreaCreateView.as_view(),name='add-microarea'),
    path('edit/<int:pk>/microarea/',micro_view.MicroAreaUpdateView.as_view(),name='edit-microarea'),
    path('list/microareas/',micro_view.MicroAreaListView.as_view(),name='list-microarea'),
    path('delete/<int:pk>/microarea/',micro_view.MicroAreaDeleteView.as_view(),name='del-microarea'),
    path('detail/<int:pk>/microarea/',micro_view.MicroAreaDetailView.as_view(),name='detail-microarea'),
]
