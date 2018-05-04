from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.auth import get_user
import json
from research.models import Transcript

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # y = dir(self.scope["user"])
        # for x in y:
        #     print(x)
        self.user = self.scope["user"]
        # self.user = await get_user(self.scope)
        # print((self.user))
        # print(self.user.username)
        # print(self.scope["path"])
        # for key, value in self.scope.items():
        # for key in self.user.items():
        #     print(key)
            # print(value)

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.transcript = Transcript(room_name=self.room_name,user=self.user)
        self.transcript.save()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = self.user.username if self.user.username != "" else "Anonymous"
        message =  username + ": " + text_data_json['message']
        # message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(dir(event))
        self.transcript.transcript += '\n' + message
        self.transcript.save()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        self.transcript.save()
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )