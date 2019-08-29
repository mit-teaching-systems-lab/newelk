from rest_framework import serializers

from .models import TFAnswer


class TFAnswerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username")
    question_text = serializers.CharField(source="question.question")

    class Meta:
        model = TFAnswer
        fields = ("user_name", "question_text", "user_answer", "correct_answer")
