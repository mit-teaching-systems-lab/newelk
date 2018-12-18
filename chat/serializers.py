from .models import ChatRoom, MessageCode, ChatNode
from rest_framework import serializers

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        # fields = ('__all__')
        fields = ('name','scenario')

class MessageCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCode
        fields = ('__all__')

class ChatNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatNode
        fields = ('__all__')