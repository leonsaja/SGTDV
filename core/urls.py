from django.urls import path

from . import views

app_name='core'
from core.views import page_not_found_view
urlpatterns = [
   path('',views.home,name='home'),

]
handler404 = 'core.views.page_not_found_view'