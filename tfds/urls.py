from django.urls import include, path

from tfds import views as view_r

app_name='tfds'
urlpatterns = [
   
     path("create/tfd/",view_r.reciboTFDCreate,name='add-recibo_tfd'),
     path("update/<int:id>/tfd/",view_r.reciboTFDUpdate,name='edit-recibo_tfd'),
     path("list/recibos_tfds/",view_r.ReciboTFDListView.as_view(),name='list-recibo_tfd'),
     path("detail/<int:pk>/tfd/",view_r.ReciboTFDDetailView.as_view(),name='detail-recibo_tfd'),
         
]
