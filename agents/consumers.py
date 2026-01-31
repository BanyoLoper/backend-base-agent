import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RealmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'global_realm'

        # Unirse al grupo del mundo virtual
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket (Cliente -> Servidor)
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # Reenviar el mensaje a todos en el grupo (Servidor -> Todos los Clientes)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'realm_message',
                'message': data
            }
        )

    # Manejador del evento del grupo
    async def realm_message(self, event):
        message = event['message']
        # Enviar mensaje al WebSocket del cliente
        await self.send(text_data=json.dumps(message))