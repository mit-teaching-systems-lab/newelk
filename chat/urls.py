from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.select_role, name='select_role'),
    path('t/', views.join_scenario, name='join_scenario'),
    path('s/', views.select_scenario, name='select_scenario'),
    path('onboard1/', views.onboard1, name='onboard1'),
    path('onboard1/', views.onboard2, name='onboard2'),
    path('onboard1/', views.onboard3, name='onboard3'),
    path('onboard1/', views.onboard4, name='onboard4'),
    path('result/', views.result, name='result'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/quiz/$', views.quiz, name='quiz'),
]