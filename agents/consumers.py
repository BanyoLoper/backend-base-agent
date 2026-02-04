import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Agent

class RealmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = 'global_realm'
        print(f"DEBUG: Conectando usuario: {self.user} - Autenticado: {self.user.is_authenticated}")
        if self.user.is_authenticated:
            # Unirse al grupo del mundo
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            
            # --- PERSISTENCIA: Cargar estado inicial del agente ---
            agent_data = await self.get_or_create_agent()
            await self.send(text_data=json.dumps({
                'type': 'initial_state',
                'agent': agent_data
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Solo intentamos salir del grupo si el usuario logró autenticarse
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # 1. Lógica del Tutorial: Asignar forma aleatoria al finalizar
        if message_type == 'finish_tutorial':
            new_shape = random.choice(['cube', 'sphere', 'pyramid'])
            await self.assign_agent_shape(new_shape)
            
            # Avisamos al usuario de su nueva forma
            await self.send(text_data=json.dumps({
                'type': 'shape_assigned',
                'shape': new_shape
            }))
            return # No necesitamos retransmitir esto a todos aún

        # 2. Lógica de Movimiento
        if 'position' in data:
            # Guardamos en la base de datos de forma persistente
            await self.update_agent_position(data['position'])

            # Retransmitimos a todos los jugadores en el Reino
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'realm_message',
                    'message': {
                        'id': str(self.user.id),
                        'position': data['position'],
                        'color': data.get('color', '#3498db'),
                        'shape': await self.get_agent_shape(), # Obtenemos la forma actual
                        'username': self.user.username
                    }
                }
            )

    async def realm_message(self, event):
        # Enviar el mensaje recibido del grupo al WebSocket del cliente
        await self.send(text_data=json.dumps(event['message']))

    # --- Métodos de Base de Datos (Decorados para Async) ---

    @database_sync_to_async
    def get_or_create_agent(self):
        # El agente ya existe gracias al Signal que configuramos al registrarse
        agent = Agent.objects.get(owner=self.user)
        return {
            'id': str(self.user.id),
            'position': [agent.pos_x, agent.pos_y, agent.pos_z],
            'color': agent.color,
            'xp': agent.xp_level,
            'shape': agent.shape # Importante para que React sepa qué renderizar
        }

    @database_sync_to_async
    def update_agent_position(self, pos):
        Agent.objects.filter(owner=self.user).update(
            pos_x=pos[0], pos_y=pos[1], pos_z=pos[2]
        )

    @database_sync_to_async
    def assign_agent_shape(self, shape):
        Agent.objects.filter(owner=self.user).update(shape=shape)

    @database_sync_to_async
    def get_agent_shape(self):
        agent = Agent.objects.get(owner=self.user)
        return agent.shape
