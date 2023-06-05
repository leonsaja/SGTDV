from django.urls import path

from transportes.views import carro_view, viagem_view

app_name='transportes'

urlpatterns = [
    # Viagem
    path('create/viagem/',viagem_view.viagemCreate,name='add-viagem'),
    path('update/<int:id>/viagem/',viagem_view.viagemUpdate,name='edit-viagem'),
    path('list/viagens/',viagem_view.ListViagemView.as_view(),name='list-viagem'),
    path('detail/<int:pk>/viagem/',viagem_view.DetailViagemView.as_view(),name='detail-viagem'),


    # Carro
    
    path('create/carro/',carro_view.CarroCreateView.as_view(),name='add-carro'),
    path('update/<int:id>/carro/',carro_view.CarroUpdateView.as_view(),name='edit-carro'),

]