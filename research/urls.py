from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.streaming_csv_view, name='csv'),
]