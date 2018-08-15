from django.contrib import admin
from .models import Scenario, TFQuestion, ChatRoom
from django.contrib.admin.sites import AdminSite

class NonStaffAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

nonstaff_admin_site = NonStaffAdmin(name='nonstaffadmin')

nonstaff_admin_site.register(ChatRoom)
nonstaff_admin_site.register(Scenario)
nonstaff_admin_site.register(TFQuestion)
