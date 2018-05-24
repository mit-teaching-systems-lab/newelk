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


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    role = models.CharField(null=True,max_length=1)
    transcript = models.ForeignKey(Transcript, on_delete=models.SET_NULL, null=True)
    creation_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        transcript_id = str(self.transcript.id) if self.transcript.id else 'no_transcript_id'
        room = self.transcript.room_name if self.transcript.room_name else 'no_room_name'
        username = self.user.username if self.user else 'System'
        role = self.role if self.role else 'role_not_set'
        time = str(self.creation_time)
        return transcript_id + ',' + room + ',' + username + ',' + role + ',' + str(self.id) + ',"' + self.text + '",' + time
