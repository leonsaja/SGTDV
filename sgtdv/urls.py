from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    
    path('administrador/', admin.site.urls),
    path("select2/", include("django_select2.urls")),

    path('',include('core.urls')),
    path('cidadao/', include('cidadao.urls')),
    path('profissionais/', include('profissionais.urls')),
    path('relatorios/',include('relatorios.urls')),
    path('estabelecimentos/', include('estabelecimentos.urls')),
    path('usuarios/',include('usuarios.urls')),
    path('tfds/',include('tfds.urls')),
    path('despesas/',include('despesas.urls')),


    path('especialidades/',include('especialidades.urls')),
    path('transportes/',include('transportes.urls')),
    #path('__debug__/', include('debug_toolbar.urls')),
   
        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


