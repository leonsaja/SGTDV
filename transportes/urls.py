from django.urls import path

from transportes.views import carro_view, viagem_view

app_name='transportes'

urlpatterns = [
    # Viagem
    path('create/viagem/',viagem_view.viagemCreate,name='add-viagem'),
    path('update/<int:id>/viagem/',viagem_view.viagemUpdate,name='edit-viagem'),
    path('list/viagens/',viagem_view.ViagemListView.as_view(),name='list-viagem'),
    path('detail/<int:pk>/viagem/',viagem_view.DetailViagemView.as_view(),name='detail-viagem'),
    path('delete/<int:pk>/viagem/',viagem_view.ViagemDeleteView.as_view(),name='del-viagem'),


    # Carro
    
    path('create/carro/',carro_view.CarroCreateView.as_view(),name='add-carro'),
    path('update/<int:pk>/carro/',carro_view.CarroUpdateView.as_view(),name='edit-carro'),
    path('list/carros/',carro_view.ListCarroView.as_view(),name='list-carro'),
    path('detail/<int:pk>/carros/',carro_view.DetailCarraView.as_view(),name='list-carro'),
]