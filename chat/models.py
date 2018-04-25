from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Scenario(models.Model):
    scenario_name = models.TextField()
    student_background = models.TextField()
    student_profile = models.TextField()
    student_hints = ArrayField(models.TextField())
    teacher_background = models.TextField()
    teacher_objective = models.TextField()
    teacher_hints = ArrayField(models.TextField())

