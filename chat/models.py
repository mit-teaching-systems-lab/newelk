from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

BOOL_CHOICES = ((True, 'True'), (False, 'False'))

class Scenario(models.Model):
    scenario_name = models.CharField(max_length=50)
    student_background = models.TextField()
    student_profile = models.TextField()
    student_hints = models.TextField(blank=True)
    teacher_background = models.TextField()
    teacher_objective = models.TextField()
    teacher_hints = models.TextField(blank=True)
    visible_to_players = models.BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    creation_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.pk + ' ' + self.scenario_name + ' ' + str(self.creation_time)

class TFQuestion(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )
    def __str__(self):
        return "Scenario: " + self.scenario.scenario_name + " Q: " + self.question

from research.models import Transcript
class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='+')
    ready_users = models.ManyToManyField(User, related_name='+')
    transcript = models.ForeignKey(Transcript,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name





# from django.db import models
# from django.contrib.postgres.fields import ArrayField
#
# # Create your models here.
# class Scenario(models.Model):
#     scenario_name = models.TextField()
#
#     def __str__(self):
#         return self.scenario_name
#
# class Teacher(models.Model):
#     scenario = models.ForeignKey(Scenario)
#     background = models.TextField()
#     objective = models.TextField()
#     hints = ArrayField(models.TextField())
#
# class Student(models.Model):
#     scenario = models.ForeignKey(Scenario)
#     background = models.TextField()
#     profile = models.TextField()
#     hints = ArrayField(models.TextField())
#
# class Observer(models.Model):
#
# class Question(models.Model):
#     question = models.TextField()
#     answers = models.
#     answer =
#     image =
#
# class Chatroom(models.Model):
#     scenario =
#     participants =
#
# class Transcript(models.Model):
    #     scenario = models.ForeignKey(Chatroom)
