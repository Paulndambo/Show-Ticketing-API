from django.urls import path
from apps.reservations.views import (
    ReservationAPIView,
    ReservationDetailAPIView,
    ReserveSeatAPIView,
    CancelReservationAPIView
)

urlpatterns = [
    path("", ReservationAPIView.as_view(), name="reservations"),
    path("<int:pk>/", ReservationDetailAPIView.as_view(), name="reservation-details"),
    path("reserve-seat/", ReserveSeatAPIView.as_view(), name="reserve-seat"),
    path("cancel-reservation/", CancelReservationAPIView.as_view(), name="cancel-reservation"),
]
