from core.models import Patrullero
from rest_framework import serializers


# class NotificadoSerializer(serializers.HyperlinkedModelSerializer):
class PatrulleroSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patrullero
		fields = ('nombre', 'cedula', 'activo', 'token')