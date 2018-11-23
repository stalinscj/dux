from django.conf import settings
# from django.db import models
# from openalpr import Alpr
import base64
import time
import json
import cv2
import os


# Create your models here.
class Lector():
	OPEN_ALPR_CONF_PATH = '/opt/openalpr/config/openalpr.conf.user'
	RUNTIME_DATA_PATH   = '/opt/openalpr/runtime_data'

	estado = 'off'

	def iniciar(self, cam_socket):

		# print("\n\nEn Iniciar estado= "+self.estado+"\n\n")
		
		if self.estado=='off':
			self.estado = 'on'
			camara = cv2.VideoCapture(0)
			success = True
			while self.estado=='on' and success==True:
				success, frame = camara.read()
				
				cam_socket.send(text_data=json.dumps({
					'tipo': 'frame',
					'img_src': self.img_to_base64(frame)
				}))

	def detener(self, cam_socket):
		# print("\n\nEn Detener estado= "+self.estado+"\n\n")
		# print("\n\nDeteniendo..\n\n");
		if self.estado=='on':
			# print("\n\nen el if\n\n");
			self.estado = 'off'
			frame = cv2.imread(os.path.join(settings.STATIC_ROOT, 'core/img/live.png'))
			time.sleep(2)
			cam_socket.send(text_data=json.dumps({
				'tipo': 'frame',
				'img_src': self.img_to_base64(frame)
			}))
			# print("\n\n...DETENIDO...\n\n");

	def img_to_base64(self, img):
		success, img_codificada = cv2.imencode('.png', img)
		if success:
			b64_src = 'data:image/png;base64,'
			img_src = b64_src + base64.b64encode(img_codificada).decode()
			return img_src

		return ''
		

		