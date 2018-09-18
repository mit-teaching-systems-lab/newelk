from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite
from mptt.admin import MPTTModelAdmin

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

class ScenarioAdmin(MPTTModelAdmin):
    # readonly_fields = ('creation_time', 'parent')
    save_as = True
    def save_model(self, request, obj, form, change):
        if change:
            print('new scenario')
            obj.visible_to_players = False
            obj.save()
            print(obj.pk)
            previous_pk = obj.pk
            obj.pk = None
            print(previous_pk)
            obj.previous_verion = Scenario.objects.get(pk=previous_pk)
            print(obj.previous_version)
            obj.save()
            # print(obj.pk)
        else:
            print('no change')

nonstaff_admin_site.register(Scenario, ScenarioAdmin)
nonstaff_admin_site.register(TFQuestion)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)