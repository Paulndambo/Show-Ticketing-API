from django.urls import path
from apps.notifications.views import add_view

urlpatterns = [
    path("add/", add_view, name="add"),
]
