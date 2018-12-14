from core.models import Patrullero
from rest_framework import viewsets
from .serializers import PatrulleroSerializer
from rest_framework import status
from rest_framework.response import Response


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
		pass

	def partial_update(self, request, pk=None):
		pass

	def destroy(self, request, pk=None):
		pass