from django.urls import path

from .views.tipo_especialidades_view import TipoEspecialidadeCreateView

app_name='especialidades'

urlpatterns = [
    
    #Tipo Especialidades
    path('create/tipoespecialidades/',  TipoEspecialidadeCreateView.as_view() , name='add-tipoespecialidades' ),  


]