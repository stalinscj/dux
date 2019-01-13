from django.shortcuts import render, get_object_or_404
from configparser import ConfigParser
from django.http import HttpResponse
from .models import Peaje
import os


def home(request):
	configurado = False
	if os.path.isfile("dux/config.ini"):
		config = ConfigParser()
		config.read('dux/config.ini')
		if config.has_option('peaje', 'id') and config.has_option('camaras', '0'):
			configurado = True

	return render(request, 'core/home.html', {'configurado': configurado})

def configuracion(request):
	peajeConfigurado = ''
	camaraConfigurada = ''

	if os.path.isfile("dux/config.ini"):
		config = ConfigParser()
		config.read('dux/config.ini')
		if config.has_option('peaje', 'id'):
			peajeConfigurado = config.getint('peaje', 'id')

		if config.has_option('camaras', '0'):
			camaraConfigurada = config.get('camaras', '0')

	params = {
		'peajeConfigurado' : peajeConfigurado,
		'camaraConfigurada' : camaraConfigurada
	}

	return render(request, 'core/configuracion.html', params)

def configurar_peaje(request):
	peaje = get_object_or_404(Peaje, pk=request.POST.get('id', 0))

	modo = 'r+' if os.path.isfile("dux/config.ini") else 'w+'

	archivo = open("dux/config.ini", mode = modo, encoding = 'utf-8')

	config = ConfigParser()

	config.read('dux/config.ini')

	if not config.has_section('peaje'):
		config.add_section('peaje')	

	config.set('peaje', 'id', str(peaje.pk))

	config.write(archivo)

	archivo.close()

	return HttpResponse(peaje.nombre)

def configurar_camara(request):
	modo = 'r+' if os.path.isfile("dux/config.ini") else 'w+'

	archivo = open("dux/config.ini", mode = modo, encoding = 'utf-8')

	config = ConfigParser()

	config.read('dux/config.ini')

	if not config.has_section('camaras'):
		config.add_section('camaras')	

	config.set('camaras', '0', request.POST.get('direccion', ''))

	config.write(archivo)

	archivo.close()

	return HttpResponse('success')