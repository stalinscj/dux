from django.urls import path
from .views import notificaciones, lecturas, patrulleros

urlpatterns = [
	#Path del Home
    path('notificaciones', notificaciones, name="notificaciones"),
    path('lecturas', lecturas, name="lecturas"),
    path('patrulleros', patrulleros, name="patrulleros"),
]