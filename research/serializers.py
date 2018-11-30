from .models import TFAnswer
from rest_framework import serializers


class TFAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TFAnswer
        fields = ('__all__')