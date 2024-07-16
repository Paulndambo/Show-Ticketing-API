from django.urls import path
from apps.reservations.views import (
    ReservationAPIView,
    ReservationDetailAPIView,
    ReserveSeatAPIView,
)

urlpatterns = [
    path("", ReservationAPIView.as_view(), name="reservations"),
    path("<int:pk>/", ReservationDetailAPIView.as_view(), name="reservation-details"),
    path("reserve-seat/", ReserveSeatAPIView.as_view(), name="reserve-seat"),
]
