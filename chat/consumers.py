from channels.generic.websocket import AsyncWebsocketConsumer
import json
from research.models import Transcript, Message
from chat.models import ChatRoom, Scenario
import re
import logging

logger = logging.getLogger(__name__)

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
        self.room_name = self.room_name.lower()

        self.room_group_name = 'chat_%s_%s' % (self.room_name, self.scenario)

        self.room = ChatRoom.objects.filter(name=self.room_name)

        if not self.room:
            self.room = ChatRoom(name=self.room_name)
            self.room.save()

            ts = Transcript(room_name=self.room_name)
            ts.scenario = Scenario.objects.get(pk=self.scenario)
            ts.save()

            self.room.transcript = ts
            self.room.save()

        else:
            self.room = self.room.order_by('-id')[0]
            # print(self.room)
            # print(self.room.transcript)
            if not self.room.transcript:
                ts = Transcript(room_name=self.room_name)
                ts.scenario = Scenario.objects.get(pk=self.scenario)
                ts.save()
                self.room.transcript = ts
                self.room.save()
        self.room.users.add(self.user)
        self.room.save()

        logger.info(self.room.transcript)

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
        if 'message' in text_data_json:
            message =  username + ": " + text_data_json['message']
            logger.info(self.room.transcript.last_line)
            logger.info(message)
            if self.room.transcript.last_line != message:
                msg_obj = Message(text=message, user=self.user, role=self.role, transcript=self.room.transcript)
                msg_obj.save()
                self.room.transcript.last_line = message

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        elif 'ready' in text_data_json:
            # Player is ready to begin
            # First add player to pool of ready players in the room
            self.room.ready_users.add(self.user)
            # If all players in the room are ready, begin timer
            logger.info(self.room.ready_users)
            logger.info(self.room.users)
            if (self.room.ready_users == self.room.users):
                # Notify everyone that the timer has begun
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': "***All players are ready, beginning timer***",
                        'begin_timer': 'true'
                    }
                )
            else:
                logger.info('Not all players ready')
        else:
            logger.info(text_data_json.keys())

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        self.room.transcript.users.add(self.user)
        self.room.users.remove(self.user)
        # print(self.room.users)
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