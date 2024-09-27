from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .models import Chatroom, Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        self.group_name= f"chat_{self.room_name}"

        await self.channel_layer.group_add( self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    @database_sync_to_async
    def get_chatroom(self, room_name):
        return Chatroom.objects.get(name= self.room_name)
    
    @database_sync_to_async
    def create_message(self, room, user, content):
        return Message.objects.create(room= room, content= content)

    async def receive(self, text_data):
        text_data_json= json.loads(text_data)
        message= text_data_json['message']
        user= self.scope["user"]

        # room= await self.get_chatroom(self.room_name)

        # await self.create_message(room,user,content= message)
        # await Message.objects.create(room=room, user=user, content= message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',

                'message': message,
                'user': user.username
            }
        )
    async def chat_message(self, event):
        Message= event['message']
        user= event['user']

        await self.send(text_data=json.dumps({
            'message': Message, 
            'user': user
        }))