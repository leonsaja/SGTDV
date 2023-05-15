from django.urls import path

from profissionais.views import (ProfissionalDeleteView,
                                 ProfissionalDetailView,
                                 ProfissionalDiariasListView,
                                 ProfissionalListView, profissionalCreate,
                                 profissionalUpdate)

app_name='profissionais'

urlpatterns = [
    #Profissional 
    path('create/profissional/', profissionalCreate, name='add-profissional' ),    
    path('update/<int:id>/profissional/', profissionalUpdate, name='edit-profissional' ), 
    path('list/profissionais/', ProfissionalListView.as_view(), name='list-profissional' ),
    path('delete/<int:pk>/profissional/', ProfissionalDeleteView.as_view(), name='del-profissional' ),
    path('detail/<int:pk>/profissional/', ProfissionalDetailView.as_view(), name='detail-profissional' ),


    #diarias
    path('list/diarias/<int:pk>/profissional/', ProfissionalDiariasListView.as_view(), name='list-diarias-profissional' ),

    

]