from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

class ScenarioAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            obj.visible_to_players = False
            obj.save()
            obj.pk = None
            obj.save()

        # super.save_model(request, obj, form, change)

admin.site.register(ChatRoom)
# admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Scenario)
admin.site.register(TFQuestion)