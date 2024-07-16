from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer, ReserveSeatSerializer
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

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)