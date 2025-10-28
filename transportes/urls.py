from django.urls import path

from transportes.views import carro_view, registro_transporte_view, viagem_view,paciente_viagem_view,destino_viagem_view

app_name='transportes'

urlpatterns = [
    
    # Viagem
    path('create/viagem',viagem_view.ViagemCreateView.as_view(),name='add-viagem'),
    path('update/<int:pk>/viagem',viagem_view.ViagemUpdateView.as_view(),name='edit-viagem'),
    path('list/viagens',viagem_view.ViagemListView.as_view(),name='list-viagem'),
    path('search/viagem',viagem_view.ViagemSearchListView.as_view(),name='search-viagem'),
    path('detail/<int:pk>/viagem',viagem_view.DetailViagemView.as_view(),name='detail-viagem'),
    path('delete/<int:pk>/viagem',viagem_view.ViagemDeleteView.as_view(),name='del-viagem'),
    path('pdf/<int:id>/viagem',viagem_view.viagemPdf, name='pdf-viagem'),
    path('buscar/paciente_viagem', paciente_viagem_view.PacienteViagemSearchView.as_view(), name='buscar-paciente-viagem' ),  


    # Carro
    
    path('create/carro',carro_view.CarroCreateView.as_view(),name='add-carro'),
    path('update/<int:pk>/carro',carro_view.CarroUpdateView.as_view(),name='edit-carro'),
    path('list/carros',carro_view.ListCarroView.as_view(),name='list-carro'),
    path('detail/<int:pk>/carros',carro_view.DetailCarraView.as_view(),name='detail-carro'),
    path('delete/<int:id>/carro',carro_view.carroDelete,name='del-carro'),
    
    
    #Registro de Transporte
    
    path('create/registro-transporte',registro_transporte_view.RegistroTransporteCreateView.as_view(),name='add-regis-transporte'),
    path('update/<int:pk>/registro-transporte',registro_transporte_view.RegistroTransporteUpdateView.as_view(),name='edit-regis-transporte'),
    path('list/registro-transportes',registro_transporte_view.RegistroTransporteListView.as_view(),name='list-regis-transporte'),
    path('detail/<int:pk>/registro-transporte',registro_transporte_view.RegistroTransporteDetailView.as_view(),name='detail-regis-transporte'),
    path('delete/<int:pk>/registro-transporte',registro_transporte_view.RegistroTransporteDeleteView.as_view(),name='del-regis-transporte'),
    path('search/registro-transporte',registro_transporte_view.RegistroTransporteSearchListView.as_view(),name='search-regis-transporte'),
    #path('importacao dados/transporte', registro_transporte_view.ImportDadosTransporteView.as_view() , name='importar-dados-transporte' ),

    path('create/destino',destino_viagem_view.DestinoViagemCreateView.as_view(),name='add-destino'),
    path('update/<int:pk>/destino',destino_viagem_view.DestinoViagemteUpdateView.as_view(),name='edit-destino'),
    path('list/destinos',destino_viagem_view.DestinoViagemListView.as_view(),name='list-destino'),
    path('destino-autocompleto',destino_viagem_view.DestinoViagemAutocomplete.as_view(),name='destino-autocompleto'),


]