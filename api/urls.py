from django.conf.urls import url, include
from rest_framework import routers
from .views import AlertaViewSet, NotificadoViewSet, PatrulleroViewSet

router = routers.DefaultRouter()
router.register(r'patrulleros', PatrulleroViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'notificados', NotificadoViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

