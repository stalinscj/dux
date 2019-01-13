from django.conf.urls import url

from .consumers import CamConsumer, ConfigConsumer

websocket_urlpatterns = [
	url(r'^ws/camara/$', CamConsumer),
	url(r'^ws/config/$', ConfigConsumer),
]