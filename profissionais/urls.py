from django.urls import path

from profissionais import views as view_profissional

app_name='profissionais'

urlpatterns = [
    #Profissional 
    path('create/profissional',view_profissional.profissionalCreate, name='add-profissional' ),    
    path('update/<int:id>/profissional', view_profissional.profissionalUpdate, name='edit-profissional' ), 
    path('delete/<int:id>/profissional', view_profissional.profissionalDelete, name='del-profissional' ),
    path('list/profissionais', view_profissional.ProfissionalListView.as_view(), name='list-profissional' ),
    path('search/profissional', view_profissional.ProfissionalSearchListView.as_view(), name='search-profissional' ),
    path('detail/<int:pk>/profissional/', view_profissional.ProfissionalDetailView.as_view(), name='detail-profissional' ),


    

]