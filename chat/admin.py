from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

class ScenarioAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time',)
    save_as = True
    def save_model(self, request, obj, form, change):
        if change:
            # print('new scenario')
            obj.visible_to_players = False
            obj.save()
            # print(obj.pk)
            previous_pk = obj.pk
            obj.pk = None
            obj.previous_verion = Scenario.objects.get(pk=previous_pk)
            obj.save()
            # print(obj.pk)

nonstaff_admin_site.register(ChatRoom)
nonstaff_admin_site.register(Scenario)
nonstaff_admin_site.register(TFQuestion)

#
# admin.site.register(ChatRoom)
# admin.site.register(Scenario, ScenarioAdmin)
# # admin.site.register(Scenario)
# admin.site.register(TFQuestion)