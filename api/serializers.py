from core.models import Alerta, Lectura, Notificacion, Patrullero, Peaje
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

class NotificacionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Notificacion
		fields = ('id', 'alerta_id', 'patrullero_id', 'entregada', 'alcanzado', 'atendida', 'fecha_entregada', 'fecha_atendida')

		

# class NotificacionSerializer(serializers.HyperlinkedModelSerializer):
class PatrulleroSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patrullero
		fields = ('id', 'nombre', 'cedula', 'activo', 'token')

class PeajeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Peaje
		fields = ('id', 'nombre', 'longitud', 'latitud', 'radio')

