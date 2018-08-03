from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

class ScenarioAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print('in admin')
        print(self)
        print(request)
        print(obj)
        for x in form:
            print(x)
        for x in change:
            print(x)
        # super.save_model(request, obj, form, change)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)