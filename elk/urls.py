"""elk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
# from django.contrib.auth.views import login, logout
from chat.admin import nonstaff_admin_site
from chat.views import ChatRoomViewSet, MessageCodeViewSet, scenario_editor, scenario_creator
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'chatroom', ChatRoomViewSet)
router.register(r'messagecode', MessageCodeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='landing_page.html'), name='home'),
    path('c/', include('consent.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('csv/', include('research.urls')),
    path('scenarios/chat/scenario/<int:pk>/change/', scenario_editor, name='scenario_editor'),
    path('scenarios/chat/scenario/add/', scenario_creator, name='scenario_creator'),
    path('scenarios/', nonstaff_admin_site.urls, name='scenario_editor'),
]

# path('accounts/login/', LoginView.as_view(), name='login'),
