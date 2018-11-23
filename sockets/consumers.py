from channels.generic.websocket import WebsocketConsumer
from alpr.models import Lector
import threading
import json



class CamConsumer(WebsocketConsumer):
	lector = None

	def connect(self):
		self.accept()

		self.lector = Lector()

		# self.lector.iniciar(self)

	def disconnect(self, close_code):
		# print("\n\nSe recibió desconexión del lciente...\n\n")
		self.lector.detener(self)

	def receive(self, text_data):
		streaming = json.loads(text_data)["data"]
		
		if streaming=='on':
			threading.Thread(target=self.lector.iniciar, args=(self,)).start()
			# self.lector.iniciar(self)

		else:
			threading.Thread(target=self.lector.detener, args=(self,)).start()
			# self.lector.detener(self)
