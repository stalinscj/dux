from core.models import Alerta, Lectura, Notificado, Patrullero
from rest_framework import serializers

class LecturaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Lectura
		fields = ('id', 'fecha', 'matricula', 'direccion', 'imagen', 'imagen_mini')

class AlertaSerializer(serializers.ModelSerializer):

	# lectura = LecturaSerializer()

	class Meta:
		model = Alerta
		fields = ('id', 'lectura_id', 'fecha')

class NotificadoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Notificado
		fields = ('id', 'alerta_id', 'patrullero_id', 'entregada', 'alcanzado', 'atendida', 'fecha_entregada', 'fecha_atendida')

		

# class NotificadoSerializer(serializers.HyperlinkedModelSerializer):
class PatrulleroSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patrullero
		fields = ('id', 'nombre', 'cedula', 'activo', 'token')

