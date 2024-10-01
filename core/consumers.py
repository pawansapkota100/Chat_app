from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Chatroom, Message
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
User= get_user_model()
# import get_or_create

class ChatConsumer(AsyncWebsocketConsumer):
    user= User.objects.first()
    
    async def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        self.group_name= f"chat_{self.room_name}"

        await self.channel_layer.group_add( self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    @database_sync_to_async
    def get_chatroom(self):
        chatroom, created = Chatroom.objects.get_or_create(name='default_room')
        return chatroom
    
    @database_sync_to_async
    def create_message(self, room, user, content):
        return Message.objects.create(room= room,user=user, content= content)

    async def receive(self, text_data):
        try:
            # Attempt to parse the incoming text data as JSON
            text_data_json = json.loads(text_data)
            
            # Safely extract 'message' and 'user' from the parsed JSON
            message = text_data_json.get('message', None)
            user = text_data_json.get('user', None)

            # Validate that both 'message' and 'user' are present
            if message is None or user is None:
                # Optionally log the error or handle it
                await self.send(text_data=json.dumps({
                    'error': "Invalid data: 'message' or 'user' missing."
                }))
                return

            # If the message and user are valid, send the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user,
                }
            )

        except json.JSONDecodeError:
            # Handle the case where the text data is not valid JSON
            await self.send(text_data=json.dumps({
                'error': "Received data is not valid JSON."
            }))
    async def chat_message(self, event):
        Message= event['message']
        user= event['user']

        await self.send(text_data=json.dumps({
            'message': Message, 
            'user': user
        }))