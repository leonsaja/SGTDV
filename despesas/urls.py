from django.urls import path

from despesas.views import reembolso_view as reem_view

from .views import diaria_view as diaria_view


app_name='despesas'

urlpatterns = [
    
    #Diária
    path('create/diaria/',diaria_view.DiariaCreateView.as_view(),name='add-diaria'),
    path('update/<int:pk>/diaria/',diaria_view.DiariaUpdateView.as_view(), name='edit-diaria'),
    path('delete/<int:id>/diaria/',diaria_view.diariaDelete,name='del-diaria'),
    path('detail/<int:pk>/diaria/',diaria_view.DiariaDetailView.as_view(),name='detail-diaria'),
    path('list/diarias/',diaria_view.DiariaListView.as_view(),name='list-diaria'),

    #Reembolsos
    path('create/<int:id>/reembolso/',reem_view.reembolsoCreate,name='add-reembolso'),
    path('update/<int:id>/reembolso/',reem_view.reembolsoUpdate,name='edit-reembolso'),
    path('delete/<int:pk>/reembolso/',reem_view.ReembolsoDeleteView.as_view(),name='del-reembolso'),
    path('detail/<int:pk>/reembolso/',reem_view.ReembolsoDetailView.as_view(),name='detail-reembolso'),
    path('list/reembolsos/',reem_view.ReembolsoListView.as_view(),name='list-reembolso'),




]
