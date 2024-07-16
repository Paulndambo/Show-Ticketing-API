from django.urls import path
from apps.ticketing.views import (
    TheatreAPIView,
    TheaterDetailAPIView,
    TheaterSeatingAPIView,
    TheaterSeatingDetailAPIView,
    ShowsAPIView,
    ShowDetailAPIView,
)

urlpatterns = [
    # Theater routes
    path("", TheatreAPIView.as_view(), name="theaters"),
    path("<int:pk>/", TheaterDetailAPIView.as_view(), name="theater-details"),
    # Shows routes
    path("shows/", ShowsAPIView.as_view(), name="shows"),
    path("shows/<int:pk>/", ShowDetailAPIView.as_view(), name="show-details"),
    # Seating routes
    path("seatings/", TheaterSeatingAPIView.as_view(), name="seatings"),
    path(
        "seatings/<int:pk>/",
        TheaterSeatingDetailAPIView.as_view(),
        name="seating-deatils",
    ),
]
