from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from urllib.parse import quote as urlquote
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib import messages

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

class ScenarioAdmin(MPTTModelAdmin):
    readonly_fields = ('creation_time', 'parent')
    # mptt_indent_field = "name"
    # save_as = True
    def response_change(self, request, obj):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        msg_dict = {
            'name': opts.verbose_name,
            'obj': format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }
        if "_continue" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
        change_url = reverse('admin:chat_scenario_change', args=(obj.id,))
        return HttpResponseRedirect(redirect_url)
        return redirect(change_url)
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