from .views import home, configuracion, configurar_peaje, configurar_camara, get_alerta_detalle
from django.conf import settings
from django.urls import path

urlpatterns = [
	#Path del Home
    path('', home, name="home"),
    path('configuracion', configuracion, name="configuracion"),
    path('configurar_peaje', configurar_peaje, name="configurar_peaje"),
    path('configurar_camara', configurar_camara, name="configurar_camara"),
    path('get_alerta_detalle', get_alerta_detalle, name="get_alerta_detalle"),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)