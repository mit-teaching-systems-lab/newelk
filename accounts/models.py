from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from chat.models import ChatNode

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    last_node = models.ForeignKey(ChatNode, null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


