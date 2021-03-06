from django.urls import path, include

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path("", include("allauth.urls")),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
]
