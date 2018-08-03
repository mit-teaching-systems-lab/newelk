from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom

class ScenarioAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # if change:
        #     newobj =
        print(str(change))
        print('in admin')
        print(request)
        print(obj)
        print(obj.pk)
        print(type(form))
        print(form.changed_data)
        # for x in form:
        #     print(x)
        # super.save_model(request, obj, form, change)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)