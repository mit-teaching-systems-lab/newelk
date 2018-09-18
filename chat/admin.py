from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite
from mptt.admin import MPTTModelAdmin
import copy

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

class ScenarioAdmin(MPTTModelAdmin):
    # readonly_fields = ('creation_time', 'parent')
    # save_as = True
    # mptt_level_indent = 200
    def save_model(self, request, obj, form, change):
        print('new scenario')

        if change:
            # editing an object
            print('scene edited')
            old_obj = Scenario.objects.get(pk=obj.pk)
            new_obj = obj
            new_obj.pk = None
            new_obj.parent = old_obj
            new_obj.save()

            old_obj.visible_to_players = False
            old_obj.save()

        else:
            # new object
            print('new scene')
            obj.save()

nonstaff_admin_site.register(Scenario, ScenarioAdmin)
nonstaff_admin_site.register(TFQuestion)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)