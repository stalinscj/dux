from django.conf import settings
# from django.db import models
from openalpr import Alpr
import base64
import time
import json
import cv2
import os


# Create your models here.
class Lector():
	OPEN_ALPR_CONF_PATH = '/opt/openalpr/config/openalpr.conf.user'
	RUNTIME_DATA_PATH   = '/opt/openalpr/runtime_data'

	estado = None
	alpr   = None

	def __init__(self):
		self.estado = 'off'
		self.alpr   = Alpr("us", self.OPEN_ALPR_CONF_PATH, self.RUNTIME_DATA_PATH)
		self.alpr.set_top_n(1)


	def iniciar(self, cam_socket):

		if self.estado=='off':
			self.estado = 'on'
			placas_candidatas = []
			tiempo_post_lectura = 1
			tiempo_ultima_lectura = 0
			camara      = cv2.VideoCapture(0)
			success     = True
			while self.estado=='on' and success==True:
				success, frame = camara.read()

				if time.time() - tiempo_ultima_lectura > tiempo_post_lectura:
					leyendo = False
				else:
					leyendo = True

				if not leyendo and placas_candidatas:
					placa = self.get_placa(placas_candidatas)
					# self.guardar_placa(placa)
					self.enviar_placa(placa, cam_socket)
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
				placa_candidata = (placa, confianza, img_placa)
				cv2.rectangle(frame, (x0-5, y0-5), (x2+5, y2+5), (0,255,0), 3)

				return placa_candidata

		return None

	def validar_placa(self, placa):
		if len(placa)>5 and  len(placa)<8:
			return True
		else:
			return False

	def get_placa(self, placas_candidatas):
		max_confianza = 0

		for i in range(0, len(placas_candidatas)):
			confianza = placas_candidatas[i][1]

			if(confianza>max_confianza):
				max_confianza = confianza
				placa = placas_candidatas[i]

		return placa

	def enviar_placa(self, placa, cam_socket):
		cam_socket.send(text_data=json.dumps({
			'tipo'    : 'tupla',
			'fecha'   : time.strftime("%d/%m/%Y %H:%M:%S"),
			'placa'   : placa[0],
			'img_src' : self.img_to_base64(placa[2]),
			'avisos'  : 0
		}))