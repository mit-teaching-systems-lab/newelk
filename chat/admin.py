from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

admin.site.register(ChatRoom)
admin.site.register(Scenario)
admin.site.register(TFQuestion)