from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Feedback(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class ChatNode(MPTTModel):
    name = models.CharField(max_length=250, blank=True)
    type = models.CharField(max_length=50, blank=True)
    message_text = models.TextField(blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT)
    feedback_link = models.ForeignKey(Feedback, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ChatNode.objects.rebuild()
        super(ChatNode, self).save(*args, **kwargs)


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
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT)
    owner = models.ForeignKey('accounts.CustomUser', null=True, on_delete=models.SET_NULL)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.scenario_name + '  /  id:' + str(self.pk) + '  /  ' + str(self.creation_time)[5:19] + ' / ' + str(self.owner)


class TFQuestion(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )

    def __str__(self):
        return "Scenario: " + self.scenario.scenario_name + ' #' + str(self.scenario.pk) + "/ Q: " + self.question


from research.models import Transcript, Message


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField('accounts.CustomUser', related_name='+')
    ready_users = models.ManyToManyField('accounts.CustomUser', related_name='+')
    scenario = models.ForeignKey(Scenario, on_delete=models.SET_NULL, null=True)
    transcript = models.ForeignKey(Transcript, on_delete=models.SET_NULL, null=True)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class MessageCode(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    other_id = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.CustomUser', null=True, on_delete=models.SET_NULL, blank=True)


class TFNode(MPTTModel):
    question = models.CharField(max_length=250, blank=True)
    answer = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )
    feedback = models.TextField(blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        TFNode.objects.rebuild()
        super(TFNode, self).save(*args, **kwargs)


class OnboardLevel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    tf_tree = models.ForeignKey(TFNode, on_delete=models.PROTECT, null=True, blank=True)
    instructions_left = models.TextField(blank=True)
    instructions_right = models.TextField(blank=True)
    profile = models.TextField(blank=True)
    chat_tree = models.ForeignKey(ChatNode, on_delete=models.PROTECT, null=True, blank=True)
