from django.contrib import admin
from .models import Transcript, TFAnswer, Message

admin.site.register(Transcript)
admin.site.register(TFAnswer)
admin.site.register(Message)