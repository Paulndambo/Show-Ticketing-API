from django.urls import path
from apps.ticketing.views import TheatreAPIView, TheaterDetailAPIView

urlpatterns = [
    path("", TheatreAPIView.as_view(), name="theaters"),
    path("<int:pk>/", TheaterDetailAPIView.as_view(), name="theater-details"),
]
