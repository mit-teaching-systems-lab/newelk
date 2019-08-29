from rest_framework import serializers

from .models import ChatRoom, MessageCode, ChatNode


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ("name", "scenario")


class MessageCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCode
        fields = "__all__"


class ChatNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField("list_children")

    def list_children(self, node):
        child_pks = {}
        for child in node.get_children():
            child_pks[child.pk] = [child.name, child.message_text]
        return child_pks

    class Meta:
        model = ChatNode
        fields = "__all__"
