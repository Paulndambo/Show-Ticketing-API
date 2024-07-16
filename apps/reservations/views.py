from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer, ReserveSeatSerializer, CancelReservationSerializer
from apps.ticketing.models import TheaterSeating
from apps.reservations.methods.reserve_seat import SeatReservationMixin
from apps.reservations.methods.cancel_reservation import CancelReservationMixin


# Create your views here.
class ReservationAPIView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    lookup_field = "pk"


class ReserveSeatAPIView(generics.CreateAPIView):
    serializer_class = ReserveSeatSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            seats_ids = data.get("seats")
            seats = TheaterSeating.objects.filter(id__in=seats_ids, booked=True)
            if seats:
                return Response(
                    {"error": "One seats is already booked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            mixin = SeatReservationMixin(data=data, user=user)
            mixin.run()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelReservationAPIView(generics.CreateAPIView):
    serializer_class = CancelReservationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            mixin = CancelReservationMixin(data=data, user=user)
            mixin.run()
            return Response({ "message": "Reservation cancelled successfully" }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)