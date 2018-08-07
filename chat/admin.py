from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

class ScenarioAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time',)
    ModelAdmin.save_as = True
    def save_model(self, request, obj, form, change):
        if change:
            print('new scenario')
            obj.visible_to_players = False
            obj.save()
            print(obj.pk)
            obj.pk = None
            obj.save()
            print(obj.pk)

        # super.save_model(request, obj, form, change)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
# admin.site.register(Scenario)
admin.site.register(TFQuestion)