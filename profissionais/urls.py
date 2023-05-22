from django.urls import path

from profissionais.views import (ProfissionalDetailView,
                                 ProfissionalDiariaListView,
                                 ProfissionalListView, profissionalCreate,
                                 profissionalDelete, profissionalUpdate)

app_name='profissionais'

urlpatterns = [
    #Profissional 
    path('create/profissional/', profissionalCreate, name='add-profissional' ),    
    path('update/<int:id>/profissional/', profissionalUpdate, name='edit-profissional' ), 
    path('list/profissionais/', ProfissionalListView.as_view(), name='list-profissional' ),
    path('delete/<int:id>/profissional/', profissionalDelete, name='del-profissional' ),
    path('detail/<int:pk>/profissional/', ProfissionalDetailView.as_view(), name='detail-profissional' ),

    #diarias
    path('list/diarias/<int:pk>/profissional/', ProfissionalDiariaListView.as_view(), name='list-diarias-profissional' ),

    

]