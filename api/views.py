from core.models import Notificado
from rest_framework import viewsets
from .serializers import NotificadoSerializer
# from rest_framework import status
from rest_framework.response import Response


class NotificadoViewSet(viewsets.ModelViewSet):
	serializer_class = NotificadoSerializer
	queryset = Notificado.objects.all().order_by('-id')

	def list(self, request):
		print(self.queryset)
		return Response({"msg":'s', 'status':200})
		# return Response ({'msg': 'Dog fed', 'status'=status.HTTP_200_OK})

	def create(self, request):
		pass

	def retrieve(self, request, pk=None):
		pass

	def update(self, request, pk=None):
		pass

	def partial_update(self, request, pk=None):
		pass

	def destroy(self, request, pk=None):
		pass