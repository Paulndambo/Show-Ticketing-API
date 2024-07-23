from django.urls import path
from apps.reservations.views import (
    ReservationAPIView,
    ReservationDetailAPIView,
    ReserveSeatAPIView,
    CancelReservationAPIView,
    MovieTicketAPIView,
    MovieTicketDetailAPIView,
)

urlpatterns = [
    path("", ReservationAPIView.as_view(), name="reservations"),
    path("<int:pk>/", ReservationDetailAPIView.as_view(), name="reservation-details"),
    path("reserve-seat/", ReserveSeatAPIView.as_view(), name="reserve-seat"),
    path(
        "cancel-reservation/",
        CancelReservationAPIView.as_view(),
        name="cancel-reservation",
    ),
    path("tickets/", MovieTicketAPIView.as_view(), name="tickets"),
    path(
        "tickets/<int:pk>/", MovieTicketDetailAPIView.as_view(), name="ticket-details"
    ),
]
