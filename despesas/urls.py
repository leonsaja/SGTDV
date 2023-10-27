from django.urls import path

from despesas.views import reembolso_view as reem_view

from .views import diaria_view as diaria_view

app_name='despesas'

urlpatterns = [
    
    #Diária
    path('diaria/create',diaria_view.DiariaCreateView.as_view(),name='add-diaria'),
    path('diaria/update/<int:pk>',diaria_view.DiariaUpdateView.as_view(), name='edit-diaria'),
    path('diaria/delete/<int:id>',diaria_view.diaria_delete,name='del-diaria'),
    path('diaria/detail/<int:pk>',diaria_view.DiariaDetailView.as_view(),name='detail-diaria'),
    path('diaria/list',diaria_view.DiariaListView.as_view(),name='list-diaria'),
    path('diaria/search',diaria_view.DiariaSearchListView.as_view(),name='search-diaria'),
    path('diaria/<int:id>/pdf',diaria_view.diaria_pdf,name='pdf-diaria'),


    #Reembolsos
    path('reembolso/create/<int:id>',reem_view.reembolso_create,name='add-reembolso'),
    path('reembolso/update/<int:id>',reem_view.reembolso_update,name='edit-reembolso'),
    path('reembolso/detail/<int:pk>',reem_view.ReembolsoDetailView.as_view(),name='detail-reembolso'),
    path('reembolso/list',reem_view.ReembolsoListView.as_view(),name='list-reembolso'),
    path('reembolso/search',reem_view.ReembolsoSearchListView.as_view(),name='search-reembolso'),
    path('reembolso/<int:id>/pdf',reem_view.reembolso_pdf,name='pdf-reembolso'),




]
