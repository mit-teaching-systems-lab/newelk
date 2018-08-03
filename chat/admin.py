from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

class ScenarioAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(self)
        print(request)
        print(obj)
        print(form)
        print(change)
        super.save_model(request, obj, form, change)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)