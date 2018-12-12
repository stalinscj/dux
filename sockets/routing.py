from django.conf.urls import url

from .consumers import CamConsumer

websocket_urlpatterns = [
	url(r'^ws/camara/$', CamConsumer),
]