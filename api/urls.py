from django.conf.urls import url, include
from rest_framework import routers
from .views import NotificadoViewSet

router = routers.DefaultRouter()
router.register(r'notificados', NotificadoViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

