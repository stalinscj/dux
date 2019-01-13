from django.urls import path
from .views import home, configuracion, configurar_peaje, configurar_camara

urlpatterns = [
	#Path del Home
    path('', home, name="home"),
    path('configuracion', configuracion, name="configuracion"),
    path('configurar_peaje', configurar_peaje, name="configurar_peaje"),
    path('configurar_camara', configurar_camara, name="configurar_camara"),
]