from django.urls import path

from tfds.views import recibo_passagem_view as view_r_p
from tfds.views import recibo_tfd_view as view_r_t
from tfds.views import procedimento_view as view_proced

app_name='tfds'
urlpatterns = [
   
     #Recibo de TFDs
     path("recibo-tfd/create/recibo-tfd",view_r_t.ReciboTFDCreateView.as_view(),name='add-recibo_tfd'),
     path("recibo-tfd/update/<int:pk>/recibo-tfd",view_r_t.ReciboTFDUpdateView.as_view(),name='edit-recibo_tfd'),
     path("recibo-tfd/update/<int:id>/status",view_r_t.reciboStatusUpdate,name='status-recibo-tfd'),
     path("recibo-tfd/list/recibos-tfds",view_r_t.ReciboTFDListView.as_view(),name='list-recibo_tfd'),
     path("recibo-tfd/search/recibo-tfd",view_r_t.ReciboTFDSearchListView.as_view(),name='search-recibo_tfd'),
     path("recibo-tfd/detail/<int:pk>/recibo-tfd/",view_r_t.ReciboTFDDetailView.as_view(),name='detail-recibo_tfd'),
     path("recibo-tfd/delete/<int:pk>/recibo-tfd",view_r_t.ReciboTFDDeleteView.as_view(),name='del-recibo_tfd'),
     path("recibo-tfd/pdf/<int:id>/recibo-tfd",view_r_t.reciboTFD_pdf,name='pdf-recibo_tfd'),

     #Recibo de Passagens TFDs
     path("create/recibo-passagem",view_r_p.ReciboPassagemCreateView.as_view(),name='add-recibo_passagem'),
     path("update/<int:pk>/recibo-passagem",view_r_p.ReciboPassagemUpdateView.as_view(),name='edit-recibo_passagem'),
     path("list/recibos-passagens",view_r_p.ReciboPassagemListView.as_view(),name='list-recibo_passagem'),
     path("search/recibo-passagem",view_r_p.ReciboPassagemSearchListView.as_view(),name='search-recibo_passagem'),
     path("detail/<int:pk>/recibo-passagem",view_r_p.ReciboPassagemDetailView.as_view(),name='detail-recibo_passagem'),
     path("delete/<int:pk>/recibo-passagen",view_r_p.ReciboPassagemDeleteView.as_view(),name='del-recibo_passagem'),
     path("pdf/<int:id>/recibo-passagem",view_r_p.reciboPassagemPdf,name='pdf-recibo_passagem'),

     #Procedimento
     path("create/procedimento",view_proced.ProcedimentoCreateView.as_view() ,name='add-procedimento'),
     path("list/procedimentos",view_proced.ProcedimentosListView.as_view() ,name='list-procedimento'),
     path("update/<int:pk>/procedimento",view_proced.ProcedimentoUpdateView.as_view() ,name='edit-procedimento'),
     path("detail/<int:pk>/procedimento",view_proced.ProcedimentosDetailView.as_view() ,name='detail-procedimento'),
     path("del/<int:id>/procedimento",view_proced.procedimentosDelete,name='del-procedimento'),
     path("search/procedimento",view_proced.ProcedimentoSearchListView.as_view() ,name='search-procedimento'),

]
