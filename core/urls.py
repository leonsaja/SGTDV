from django.urls import path

from . import views

app_name='core'
from core.views import page_not_found_view
urlpatterns = [
   path('',views.home,name='home'),
   #path('agenda', views.calendar_view, name='agenda_view'),
   #path('api/events/', views.event_list_create, name='event_list_create'),
   #path('api/events/<int:pk>/', views.event_detail, name='event_detail'),

]
handler404 = 'core.views.page_not_found_view'