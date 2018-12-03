from django.urls import path
from . import views

urlpatterns = [
    # path('chatlogs/', views.streaming_chat_csv),
    # path('answerlogs/', views.streaming_answers_view),
    path('feedback/', views.toggle_feedback),
]