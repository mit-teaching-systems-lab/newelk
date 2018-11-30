from .models import TFAnswer
from rest_framework import serializers


class TFAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFAnswer
        user_name = serializers.CharField(source='user.name')
        fields = ('user_name','question','user_answer','correct_answer')