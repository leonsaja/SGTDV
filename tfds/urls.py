from django.urls import path

from tfds.views import recibo_passagem_view as view_r_p
from tfds.views import recibo_tfd_view as view_r_t
from tfds.views import procedimento_view as view_proced

app_name='tfds'
urlpatterns = [
   
     #Recibo de TFDs
     path("create/recibo-tfd",view_r_t.reciboTFDCreate,name='add-recibo_tfd'),
     path("update/<int:id>/recibo-tfd",view_r_t.reciboTFDUpdate,name='edit-recibo_tfd'),
     path("list/recibos-tfds",view_r_t.ReciboTFDListView.as_view(),name='list-recibo_tfd'),
     path("search/recibo-tfd",view_r_t.ReciboTFDSearchListView.as_view(),name='search-recibo_tfd'),
     path("detail/<int:pk>/recibo-tfd/",view_r_t.ReciboTFDDetailView.as_view(),name='detail-recibo_tfd'),
     path("delete/<int:pk>/recibo-tfd",view_r_t.ReciboTFDDeleteView.as_view(),name='del-recibo_tfd'),
     path("pdf/<int:id>/recibo-tfd",view_r_t.reciboTfdPdf,name='pdf-recibo_tfd'),

     #Recibo de Passagens TFDs

     path("create/recibo-passagem",view_r_p.ReciboPassagemCreateView.as_view(),name='add-recibo_passagem'),
     path("update/<int:pk>/recibo-passagem",view_r_p.ReciboPassagemUpdateView.as_view(),name='edit-recibo_passagem'),
     path("list/recibos-passagens",view_r_p.ReciboPassagemListView.as_view(),name='list-recibo_passagem'),
     path("search/recibo-passagem",view_r_p.ReciboPassagemSearchListView.as_view(),name='search-recibo_passagem'),
     path("detail/<int:pk>/recibo-passagem",view_r_p.ReciboPassagemDetailView.as_view(),name='detail-recibo_passagem'),
     path("delete/<int:pk>/recibo-passagen",view_r_p.ReciboPassagemDeleteView.as_view(),name='del-recibo_passagem'),
     path("pdf/<int:id>/recibo-passagem",view_r_p.reciboPassagemPdf,name='pdf-recibo_passagem'),


     #procedimento
     path("create/procedimento",view_proced.ProcedimentoCreateView.as_view() ,name='add-procedimento'),
     path("list/procedimentos",view_proced.ProcedimentosListView.as_view() ,name='list-procedimento'),



]
