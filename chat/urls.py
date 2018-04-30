from django.conf.urls import url
from django.contrib.auth.views import LoginView


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^(login/$', LoginView.as_view()),
]