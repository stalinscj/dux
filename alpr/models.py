from core.models import Alerta, Lectura, MatriculaSolicitada, Peaje
from configparser import ConfigParser
from django.conf import settings
# from django.db import models
from openalpr import Alpr
import numpy as np
import threading
import base64
import time
import json
import uuid
import cv2
import os


# Create your models here.
class Lector():
	OPEN_ALPR_CONF_PATH = '/opt/openalpr/config/openalpr.conf.user'
	RUNTIME_DATA_PATH   = '/opt/openalpr/runtime_data'

	estado = None
	alpr   = None

	estado_config = None

	def __init__(self):
		self.estado = 'off'
		self.alpr   = Alpr("us", self.OPEN_ALPR_CONF_PATH, self.RUNTIME_DATA_PATH)
		self.alpr.set_top_n(1)


	def iniciar(self, cam_socket):

		if self.estado=='off':
			self.estado           = 'on'
			placas_candidatas     = []
			tiempo_post_lectura   = 1
			tiempo_ultima_lectura = 0
			# camara              = cv2.VideoCapture(0)
			camara                = cv2.VideoCapture('/home/stalinscj/_dux_test/test/vehiculoTest/portonOriginalSinBorde_640x360.mp4')
			
			leyendo               = False
			success               = True
			# video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 20, (640,360))
			while self.estado=='on' and success==True:
				success, frame = camara.read()

				if not success:
					break

				if time.time() - tiempo_ultima_lectura > tiempo_post_lectura:
					if leyendo==True:
						video.release()
						threading.Thread(target=self.guardar_video, args=(video_nombre,)).start()
					leyendo = False
					

				else:
					if leyendo==False:
						video_nombre = "media/{0}.mp4".format(uuid.uuid4().int & (1<<64)-1)
						#MP4V
						# 0x7634706d
						# video = cv2.VideoWriter(video_nombre, cv2.VideoWriter_fourcc(*'MP4V'), 20, (640,360))
						video = cv2.VideoWriter(video_nombre, 0x7634706d, 20, (640,360))
					
					leyendo = True
					video.write(frame)

				if not leyendo and placas_candidatas:
					placa = self.get_placa(placas_candidatas)
					threading.Thread(target=self.procesar_envio, args=(placa, cam_socket, video_nombre,)).start()
					del placas_candidatas[:]

				placa_candidata = self.buscar_placa(frame)

				if placa_candidata:
					placas_candidatas.append(placa_candidata)
					tiempo_ultima_lectura = time.time()
				
				cam_socket.send(text_data=json.dumps({
					'tipo'    : 'frame',
					'img_src' : self.img_to_base64(frame)
				}))

			

	def detener(self, cam_socket):
		if self.estado=='on':
			self.estado = 'off'
			frame = cv2.imread(os.path.join(settings.STATIC_ROOT, 'core/img/live.png'))
			time.sleep(2)
			cam_socket.send(text_data=json.dumps({
				'tipo': 'frame',
				'img_src': self.img_to_base64(frame)
			}))

	def img_to_base64(self, img):
		success, img_codificada = cv2.imencode('.png', img)
		if success:
			b64_src = 'data:image/png;base64,'
			img_src = b64_src + base64.b64encode(img_codificada).decode()
			return img_src

		return ''

	def buscar_placa(self, frame):
		buscador  = self.alpr.recognize_ndarray(frame)
		resultado = buscador['results'] 

		if(resultado):
			placa = resultado[0]['plate']
			if self.validar_placa(placa):
				confianza       = resultado[0]['confidence']
				coordenadas     = resultado[0]['coordinates']
				x0              = coordenadas[0]['x']
				y0              = coordenadas[0]['y']	
				x2              = coordenadas[2]['x']
				y2              = coordenadas[2]['y']
				img_placa       = frame[y0:y2, x0:x2]
				placa_candidata = (placa, confianza, img_placa, frame)
				cv2.rectangle(frame, (x0-5, y0-5), (x2+5, y2+5), (0,255,0), 3)

				return placa_candidata

		return None

	def validar_placa(self, placa):
		if len(placa)>5 and  len(placa)<8:
			return True
		else:
			return False

	def filtrar_placas(self, placas_candidatas):
		flag = False
		for placa in placas_candidatas:
			if len(placa[0]) > 6:
				flag = True
				break

		if flag:
			for placa in placas_candidatas:
				if len(placa[0]) < 7:
					placas_candidatas.remove(placa)



	def get_placa(self, placas_candidatas):

		self.filtrar_placas(placas_candidatas)

		max_confianza = 0

		for i in range(0, len(placas_candidatas)):
			confianza = placas_candidatas[i][1]

			if(confianza>max_confianza):
				max_confianza = confianza
				placa = placas_candidatas[i]

		return placa

	def procesar_envio(self, placa, cam_socket, video_nombre):
		placa_str      = placa[0]
		placa_img      = placa[3]
		placa_img_mini = placa[2]

		config = ConfigParser()

		config.read('dux/config.ini')

		peaje = Peaje.objects.filter(pk=config.get('peaje', 'id')).first()

		lectura = Lectura.objects.create (
			peaje       = peaje,
			matricula   = placa_str,
			direccion   = config.get('camaras', '0'),
			imagen      = self.img_to_base64(placa_img),
			imagen_mini = self.img_to_base64(placa_img_mini),
			video       = video_nombre
		)

		solicitud = MatriculaSolicitada.objects.filter(matricula=placa_str, activo=True).first()
		
		avisos = 0
		idAlerta = ''
		if solicitud:
			alerta = Alerta.nueva(solicitud, lectura)
			idAlerta = alerta.pk
			avisos = alerta.notificacion_set.all().count()

		cam_socket.send(text_data=json.dumps({
			'tipo'      : 'tupla',
			'fecha'     : time.strftime("%d/%m/%Y %H:%M:%S"),
			'placa'     : placa_str,
			'img_src'   : self.img_to_base64(placa_img_mini),
			'avisos'    : avisos,
			'alerta_id' : idAlerta
		}))

	def iniciar_config(self, cam_socket):
		self.estado_config = 'on'
		camara = cv2.VideoCapture(0)
		success = True
		while self.estado_config=='on' and success==True:
			success, frame = camara.read()

			if not success:
				break
			cam_socket.send(text_data=json.dumps({
				'img_src' : self.img_to_base64(frame)
			}))

	def terminar_config(self, cam_socket):
		if self.estado_config=='on':
			self.estado_config = 'off'
			frame = cv2.imread(os.path.join(settings.STATIC_ROOT, 'core/img/live.png'))
			time.sleep(2)
			cam_socket.send(text_data=json.dumps({
				'img_src': self.img_to_base64(frame)
			}))

	def guardar_video(self, video_nombre):
		os.system("ffmpeg -i {0}.mp4 -loglevel quiet -an -vcodec libx264 -crf 23 {0}tmp.mp4".format(video_nombre[:-4]))
		os.system("rm -f "+video_nombre)
		os.system("mv {0}tmp.mp4 {0}.mp4".format(video_nombre[:-4]))
