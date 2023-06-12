from django.urls import path

from tfds.views import recibo_passagem_view as view_r_p
from tfds.views import recibo_tfd_view as view_r_t

app_name='tfds'
urlpatterns = [
   
     #Recibo de TFDs
     path("create/recibo-tfd/",view_r_t.reciboTFDCreate,name='add-recibo_tfd'),
     path("update/<int:id>/tfd/",view_r_t.reciboTFDUpdate,name='edit-recibo_tfd'),
     path("list/recibos_tfds/",view_r_t.ReciboTFDListView.as_view(),name='list-recibo_tfd'),
     path("detail/<int:pk>/tfd/",view_r_t.ReciboTFDDetailView.as_view(),name='detail-recibo_tfd'),
         

     #Recibo de Passagens TFDs

     path("create/recibo-passagem/",view_r_p.ReciboPassagemTFDCreateView.as_view(),name='add-recibo_passagem'),
     path("update/<int:pk>/recibo-passagem/",view_r_p.ReciboPassagemTFDUpdateView.as_view(),name='edit-recibo_passagem'),
     path("list/recibos/passagens/",view_r_p.ListReciboPassagemTFDView.as_view(),name='list-recibo_passagem'),

]
