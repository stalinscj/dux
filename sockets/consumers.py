from channels.generic.websocket import WebsocketConsumer
from alpr.models import Lector
import threading
import json


class CamConsumer(WebsocketConsumer):
	lector = None

	def connect(self):
		self.accept()

		self.lector = Lector()

	def disconnect(self, close_code):
		self.lector.detener(self)

	def receive(self, text_data):
		streaming = json.loads(text_data)["data"]
		
		if streaming=='on':
			threading.Thread(target=self.lector.iniciar, args=(self,)).start()

		else:
			threading.Thread(target=self.lector.detener, args=(self,)).start()

class ConfigConsumer(WebsocketConsumer):
	lector = None

	def connect(self):
		self.accept()

		self.lector = Lector()

		threading.Thread(target=self.lector.iniciar_config, args=(self,)).start()

	def disconnect(self, close_code):
		# print("\n\nSe recibió desconexión CONFIG del lciente...\n\n")
		self.lector.terminar_config(self)
