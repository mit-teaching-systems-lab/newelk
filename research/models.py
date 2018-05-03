from django.db import models
from django.contrib.auth.models import User
from chat.models import Scenario
from django.utils import timezone

# Create your models here.
class Transcript(models.Model):
    users = models.ManyToManyField(User)
    transcript = models.TextField(null=True)
    room_name = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    # teacher_hints = ArrayField(models.TextField())


# class Score(models.Model):
#     scenario = models.ForeignKey(Scenario)
#     user = models.ForeignKey(User)