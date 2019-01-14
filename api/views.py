from core.models import Alerta, Notificacion, Patrullero, Peaje
from rest_framework import viewsets
from .serializers import AlertaSerializer, NotificacionSerializer, PatrulleroSerializer, PeajeSerializer
from rest_framework import status
from rest_framework.response import Response
from collections import OrderedDict
from django.utils import timezone

class PatrulleroViewSet(viewsets.ModelViewSet):
	serializer_class = PatrulleroSerializer
	queryset = Patrullero.objects.all().order_by('-id')

	def list(self, request):
		patrulleros = Patrullero.objects.all()
		serializer = PatrulleroSerializer(patrulleros, many=True)
		return Response(serializer.data)
		# return Response({"msg":'s', 'status':200})
		# return Response ({'msg': 'Dog fed', 'status'=status.HTTP_200_OK})


	def create(self, request):
		serializer = PatrulleroSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		pass

	def update(self, request, pk=None):
		token = request.data.get("token")
		patrullero = Patrullero.objects.filter(pk=pk)
		patrullero.update(token=token)
		serializer = PatrulleroSerializer(patrullero.first())
		
		return Response(serializer.data, status=status.HTTP_200_OK)

	def partial_update(self, request, pk=None):
		pass

	def destroy(self, request, pk=None):
		pass

class AlertaViewSet(viewsets.ModelViewSet):
	serializer_class = AlertaSerializer
	queryset = Alerta.objects.all().order_by('-id')

	def list(self, request):
		alertas = Alerta.objects.all()
		serializer = AlertaSerializer(alertas, many=True)
		return Response(serializer.data)


	def retrieve(self, request, pk=None):
		alerta = Alerta.objects.filter(pk=pk).first()
		if alerta:

			lectura = alerta.lectura
			alerta_detalle = OrderedDict()
			alerta_detalle['id'] = alerta.pk
			alerta_detalle['fecha'] = timezone.localtime(alerta.fecha).strftime("%Y-%m-%d %H:%m:%S")
			alerta_detalle['lectura_id'] = lectura.primary_key=True
			alerta_detalle['peaje_id'] = lectura.peaje.pk
			alerta_detalle['fecha_lectura'] = timezone.localtime(lectura.fecha).strftime("%Y-%m-%d %H:%m:%S")
			alerta_detalle['matricula'] = lectura.matricula
			alerta_detalle['direccion'] = lectura.direccion
			alerta_detalle['imagen'] = lectura.imagen
				
			return Response(alerta_detalle, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)



class NotificacionViewSet(viewsets.ModelViewSet):
	serializer_class = NotificacionSerializer
	queryset = Notificacion.objects.all().order_by('-id')

	def list(self, request):
		notificaciones = Notificacion.objects.all()
		serializer = NotificacionSerializer(notificaciones, many=True)
		return Response(serializer.data)


	def update(self, request, pk=None):
		data = request.data
		if pk is not '0':
			notificacion = Notificacion.objects.filter(pk=pk)
		else:
			idAlerta     = data["alerta_id"]
			idPatrullero = data["patrullero_id"]
			notificacion = Notificacion.objects.filter(alerta_id=idAlerta, patrullero_id=idPatrullero)

		notificacion.update(
			entregada=True if (data["entregada"]=="true") else False,
			alcanzado=True if (data["alcanzado"]=="true") else False,
			atendida=True if (data["atendida"]=="true") else False,
			fecha_entregada=data["fecha_entregada"],
			fecha_atendida=data.get("fecha_atendida", None)
		)

		serializer = NotificacionSerializer(notificacion.first())
		
		return Response(serializer.data, status=status.HTTP_200_OK)

class PeajeViewSet(viewsets.ModelViewSet):
	serializer_class = PeajeSerializer
	queryset = Peaje.objects.all().order_by('-id')

	def list(self, request):
		peajes = Peaje.objects.all()
		serializer = PeajeSerializer(peajes, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		peaje = Peaje.objects.filter(pk=pk).first()
		if peaje:
			serializer = PeajeSerializer(peaje)

			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)