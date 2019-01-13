from django.shortcuts import render
from core.models import Lectura, Notificado, Patrullero

def notificaciones(request):
	notificaciones = Notificado.objects.all()
	return render(request, 'reportes/notificaciones.html', {'notificaciones': notificaciones})


def lecturas(request):
	lecturas = Lectura.objects.all()
	return render(request, 'reportes/lecturas.html', {'lecturas': lecturas})

def patrulleros(request):
	patrulleros_raw = Patrullero.objects.all()

	patrulleros = []

	for patrullero in patrulleros_raw:
		patrullero.alcanzado = patrullero.notificado_set.filter(alcanzado=True).all().count()
		patrullero.atendido = patrullero.notificado_set.filter(atendida=True).all().count()
		patrullero.eficacia = str(round(patrullero.atendido/patrullero.alcanzado, 2)*100) + " %"

		patrulleros.append(patrullero)

	return render(request, 'reportes/patrulleros.html', {'patrulleros': patrulleros})