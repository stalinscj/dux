from django.conf.urls import url, include
from rest_framework import routers
from .views import AlertaViewSet, NotificacionViewSet, PatrulleroViewSet, PeajeViewSet

router = routers.DefaultRouter()
router.register(r'patrulleros', PatrulleroViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'peajes', PeajeViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

