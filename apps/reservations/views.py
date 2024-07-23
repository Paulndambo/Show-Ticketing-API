from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.reservations.models import Reservation, MovieTicket
from apps.reservations.serializers import (
    ReservationSerializer,
    ReserveSeatSerializer,
    CancelReservationSerializer,
    MovieTicketSerializer,
)
from apps.ticketing.models import TheaterSeating
from apps.reservations.methods.reserve_seat import SeatReservationMixin
from apps.reservations.methods.cancel_reservation import CancelReservationMixin


# Create your views here.
@method_decorator(cache_page(60*3), name='dispatch')
class MovieTicketAPIView(generics.ListCreateAPIView):
    queryset = MovieTicket.objects.all()
    serializer_class = MovieTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser or not user.is_staff:
            return queryset.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache_key = "movie_tickets_list"
        cache.delete(cache_key)
    

class MovieTicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieTicket.objects.all()
    serializer_class = MovieTicketSerializer

    lookup_field = "pk"


class ReservationAPIView(generics.ListAPIView):
    queryset = Reservation.objects.all().order_by("-created")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff or not user.is_superuser:
            return self.queryset.filter(user=user)

        return super().get_queryset()


class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all().order_by("-created")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

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
            ticket_id = serializer.validated_data.get("ticket_id")
            try:
                mixin = CancelReservationMixin(ticket_id=ticket_id, user=user)
                mixin.run()
                return Response(
                    {"message": "Reservation cancelled successfully"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                raise e
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
