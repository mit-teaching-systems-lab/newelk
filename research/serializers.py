from .models import TFAnswer
from rest_framework import serializers


class TFAnswerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='self.user.name')
    class Meta:
        model = TFAnswer
        fields = ('user_name','question','user_answer','correct_answer')