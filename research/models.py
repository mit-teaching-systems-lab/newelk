from django.db import models
from django.contrib.auth.models import User
from chat.models import Scenario
from django.utils import timezone

# Create your models here.
class Transcript(models.Model):
    # users = models.ManyToManyField(User)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    transcript = models.TextField(default="")
    room_name = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    # teacher_hints = ArrayField(models.TextField())
    def __str__(self):
        return self.users + self.creation_time


# class Score(models.Model):
#     scenario = models.ForeignKey(Scenario)
#     user = models.ForeignKey(User)