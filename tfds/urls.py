from django.urls import include, path

from tfds.views import DetailReciboTFDView, editartfd, listatfd, tfdcadastro

app_name='tfd'
urlpatterns = [
   
     path("create/tfd/",tfdcadastro,name='add-tfd'),
     path("list/tfd/",listatfd,name='list-tfd'),
     path("update/<int:id>/tfd/",editartfd,name='edit-tfd'),
     path("detail/<int:pk>/tfd/",DetailReciboTFDView.as_view(),name='detail-tfd'),


     
    
]
