from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='chat_select'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]