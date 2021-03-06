from core.models import Lectura, Notificacion, Patrullero
from django.shortcuts import render

def notificaciones(request):
	notificaciones = Notificacion.objects.all()
	return render(request, 'reportes/notificaciones.html', {'notificaciones': notificaciones})


def lecturas(request):
	lecturas = Lectura.objects.all()
	return render(request, 'reportes/lecturas.html', {'lecturas': lecturas})

def patrulleros(request):
	patrulleros_raw = Patrullero.objects.all()

	patrulleros = []

	for patrullero in patrulleros_raw:
		patrullero.alcanzado = patrullero.notificacion_set.filter(alcanzado=True).all().count()
		patrullero.atendido = patrullero.notificacion_set.filter(atendida=True).all().count()
		patrullero.eficacia = "{:.2f}".format(100*patrullero.atendido/patrullero.alcanzado) + " %" if patrullero.alcanzado else "0.00 %"

		patrulleros.append(patrullero)

	return render(request, 'reportes/patrulleros.html', {'patrulleros': patrulleros})