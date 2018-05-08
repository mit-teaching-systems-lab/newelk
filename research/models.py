from django.db import models
from django.contrib.auth.models import User
from chat.models import Scenario
from django.utils import timezone

# Create your models here.
class Transcript(models.Model):
    users = models.ManyToManyField(User)
    scenario = models.ForeignKey(Scenario,on_delete=models.SET_NULL,null=True)
    transcript = models.TextField(default="")
    last_line = models.TextField(default="")
    room_name = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    # teacher_hints = ArrayField(models.TextField())
    def __str__(self):
        try:
            name = self.room_name
        except AttributeError:
            name = "NO_ROOM_NAME"
        return name + ' ' + str(self.creation_time)[0:10]

from chat.models import TFQuestion
class TFAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    transcript = models.ForeignKey(Transcript, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(TFQuestion, on_delete=models.SET_NULL, null=True)
    user_answer = models.TextField(null=True)
    correct_answer = models.TextField(null=True)
