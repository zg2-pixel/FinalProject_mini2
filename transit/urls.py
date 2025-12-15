from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("events/new/", views.create_stop_event, name="create_stop_event"),
    path("events/", views.event_list, name="event_list"),
]
