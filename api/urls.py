from django.conf.urls import url, include
from rest_framework import routers
from .views import PatrulleroViewSet

router = routers.DefaultRouter()
router.register(r'patrulleros', PatrulleroViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

