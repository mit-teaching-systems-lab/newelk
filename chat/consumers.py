from channels.generic.websocket import AsyncWebsocketConsumer
import json
from research.models import Transcript, Message
from chat.models import ChatRoom, Scenario
import re

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # y = dir(self.scope["user"])
        # for x in y:
        #     print(x)
        self.user = self.scope["user"]
        self.role = self.scope['url_route']['kwargs']['role']
        self.scenario = self.scope['url_route']['kwargs']['scenario']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = re.sub('%', '-', self.room_name)
        self.room_name = re.sub(' ', '-', self.room_name)
        self.room_name = re.sub('_', '-', self.room_name)
        self.room_name = re.sub('!', '-', self.room_name)

        self.room_group_name = 'chat_%s_%s' % (self.room_name, self.scenario)



        self.room = ChatRoom.objects.filter(name=self.room_name)
        if not self.room:
            self.room = ChatRoom(name=self.room_name)
            self.room.save()
            self.transcript = Transcript(room_name=self.room_name)
            self.transcript.scenario = Scenario.objects.get(pk=self.scenario)
            self.transcript.save()
            self.room.transcript = self.transcript
            print('made room')

        else:
            self.room = self.room.order_by('-id')[0]
            # ensures last_line is not null
            if not self.room.transcript or not self.room.transcript.last_line:
                self.transcript = Transcript(room_name=self.room_name)
                self.transcript.scenario = Scenario.objects.get(pk=self.scenario)
                self.transcript.save()
                self.room.transcript = self.transcript
        self.room.users.add(self.user)
        # self.room.transcript.users.add(self.user)
        self.room.save()

        # self.room.transcript = Transcript(room_name=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # send join message
        username = self.user.username if self.user.username != "" else "Anonymous"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "***" + username + " has joined the room***"
            }
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

        if self.room.transcript.last_line != message:
            # self.room.transcript.transcript += message + '\n'
            self.msg_obj = Message(text=message, user=self.user, role=self.role, transcript=self.room.transcript)
            self.msg_obj.save()
            self.room.transcript.save()
        self.room.transcript.last_line = message
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        self.room.transcript.users.add(self.user)
        self.room.users.remove(self.user)
        print(self.room.users)
        if not self.room.users.all():
            # self.room.transcript.
            print('deleting')
            ChatRoom.objects.filter(pk=self.room.pk).delete()
        else:
            self.room.save()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )