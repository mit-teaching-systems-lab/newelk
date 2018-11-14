from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from accounts.models import CustomUser as User
from mptt.models import MPTTModel, TreeForeignKey

BOOL_CHOICES = ((True, 'True'), (False, 'False'))

class Scenario(MPTTModel):
    scenario_name = models.CharField(max_length=50)
    student_background = models.TextField()
    student_profile = models.TextField()
    student_hints = models.TextField(blank=True)
    teacher_background = models.TextField()
    teacher_objective = models.TextField()
    teacher_hints = models.TextField(blank=True)
    visible_to_players = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )
    # previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    parent =  TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    creation_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.scenario_name + '  /  id:' + str(self.pk) + '  /  ' +  str(self.creation_time)[5:19]


class TFQuestion(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )
    def __str__(self):
        return "Scenario: " + self.scenario.scenario_name + " Q: " + self.question

from research.models import Transcript, Message
class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='+')
    ready_users = models.ManyToManyField(User, related_name='+')
    scenario = models.ForeignKey(Scenario,on_delete=models.SET_NULL,null=True)
    transcript = models.ForeignKey(Transcript,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

class MessageCode(models.Model):
    message = models.ForeignKey(Message,on_delete=models.SET_NULL,null=True,blank=True)
    other_id = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)

