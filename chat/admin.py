from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import CustomUser as User
from django.contrib.auth.models import Group

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        g = Group.objects.get(name='scene_creators')
        g.user_set.add(request.user)
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

class ScenarioAdmin(MPTTModelAdmin):
    list_display = ('__str__', 'visible_to_players')
    readonly_fields = ('creation_time', 'parent', 'owner')
    MPTT_ADMIN_LEVEL_INDENT = 20
    def response_change(self, request, obj):
        request.path = reverse('admin:chat_scenario_change', args=(obj.id,))
        return super().response_change(request, obj)
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
            obj.owner = request.user
            obj.visible_to_players = True
            obj.save()

        Scenario.objects.partial_rebuild(obj.tree_id)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

nonstaff_admin_site.register(Scenario, ScenarioAdmin)
nonstaff_admin_site.register(TFQuestion)

admin.site.register(User)

admin.site.register(ChatRoom)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(TFQuestion)