from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('scenarios/chat/scenario/<int:pk>/change/', views.scenario_editor, name='scenario_editor'),
    url(r'^$', views.select_role, name='select_role'),
    path('t/', views.join_scenario, name='join_scenario'),
    path('s/', views.select_scenario, name='select_scenario'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/quiz/$', views.quiz, name='quiz'),
]