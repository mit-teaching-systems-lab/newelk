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

    def __str__(self):
        return self.scenario_name

# class Quiz(models.Model):
#     questions = ArrayField(models.TextField())

# class Teacher(models.Model):
#
#
# class Student(models.Model):
#
#
# class Chat(models.Model):
#
#
#
# class Quiz(models.Model):
#
#
#
#
# class Transcript(model.Models):



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
