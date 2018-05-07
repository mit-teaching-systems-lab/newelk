from django.db import models
from django.contrib.auth.models import User
# from chat.models import Scenario
from django.utils import timezone

# Create your models here.
class Transcript(models.Model):
    users = models.ManyToManyField(User)
    # user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    transcript = models.TextField(default="")
    last_line = models.TextField(default="")
    room_name = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    # teacher_hints = ArrayField(models.TextField())
    def __str__(self):
        try:
            name = self.room_name
        except AttributeError:
            name = "Anonymous"
        return name + ' ' + str(self.creation_time)[0:10]



# class Result(models.Model):
#     user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
#     scenario = models.ForeignKey(Scenario,on_delete=models.SET_NULL,null=True)
#     score = models.IntegerField()
#


# class Score(models.Model):
#     scenario = models.ForeignKey(Scenario)
#     user = models.ForeignKey(User)