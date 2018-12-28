from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.select_role, name='select_role'),
    path('t/', views.join_scenario, name='join_scenario'),
    path('s/', views.select_scenario, name='select_scenario'),
    path('menu/', views.onboard_menu, name='onboard_menu'),
    path('chatinst/', views.chat_inst, name='chat_inst'),
    path('onboard/', views.onboard_inst, name='onboard_inst'),
    path('onboard1/', views.onboard1, name='onboard1'),
    path('onboard2/', views.onboard2, name='onboard2'),
    path('onboard3/', views.onboard3, name='onboard3'),
    path('onboard4/', views.onboard4, name='onboard4'),
    path('<int:level>/singleplayerchat/', views.single_player_chat, name='single_player_chat_1'),
    path('<int:level>/singleplayerchat/<int:feedback>/', views.chat_feedback, name='single_player_chat_1'),
    path('code/', views.code_messages, name='code'),
    path('result/', views.result, name='result'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^(?P<role>[-\s\w]+)/(?P<scenario>[-\s\w]+)/(?P<room_name>[^/]+)/quiz/$', views.quiz, name='quiz'),
]