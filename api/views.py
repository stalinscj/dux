from core.models import Alerta, Notificado, Patrullero
from rest_framework import viewsets
from .serializers import AlertaSerializer, NotificadoSerializer, PatrulleroSerializer
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



class NotificadoViewSet(viewsets.ModelViewSet):
	serializer_class = NotificadoSerializer
	queryset = Notificado.objects.all().order_by('-id')

	def list(self, request):
		notificados = Notificado.objects.all()
		serializer = NotificadoSerializer(notificados, many=True)
		return Response(serializer.data)


	def update(self, request, pk=None):
		data = request.data
		if pk is not '0':
			notificado = Notificado.objects.filter(pk=pk)
		else:
			idAlerta     = data["alerta_id"]
			idPatrullero = data["patrullero_id"]
			notificado = Notificado.objects.filter(alerta_id=idAlerta, patrullero_id=idPatrullero)

		notificado.update(
			entregada=True if (data["entregada"]=="true") else False,
			alcanzado=True if (data["alcanzado"]=="true") else False,
			atendida=True if (data["atendida"]=="true") else False,
			fecha_entregada=data["fecha_entregada"],
			fecha_atendida=data.get("fecha_atendida", None)
		)

		serializer = NotificadoSerializer(notificado.first())
		
		return Response(serializer.data, status=status.HTTP_200_OK)