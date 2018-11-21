from channels.generic.websocket import WebsocketConsumer
import json

class PrincipalCamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'message': "Éxito!!!",
        }))

    def disconnect(self, close_code):
        pass
