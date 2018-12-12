from core.models import Notificado
from rest_framework import serializers


# class NotificadoSerializer(serializers.HyperlinkedModelSerializer):
class NotificadoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notificado
		fields = ('alerta', 'patrullero')