from django.shortcuts import render
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response


from apps.ticketing.models import Theater, TheaterSeating, Show
from apps.ticketing.serializers import (
    TheaterSerializer,
    TheaterSeatingSerializer,
    ShowSerializer,
    ShowListSerializer,
    CreateShowSerializer,
)
from apps.ticketing.methods.create_show import CreateShowMixin

from apps.core.custom_permissions import IsAdminOrReadOnly


# Create your views here.
class TheatreAPIView(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):

        specified_date = self.request.query_params.get("date")

        if specified_date:
            search_date = datetime.strptime(specified_date, "%Y-%m-%d").date()
            seatings = (
                TheaterSeating.objects.filter(seating_date=search_date)
                .values_list("theater_id", flat=True)
                .distinct()
            )
            return self.queryset.exclude(id__in=seatings)
        return super().get_queryset()


class TheaterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


## Shows views
class ShowsAPIView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        user = self.request.user
        if self.request.method in ["POST", "post"]:
            return CreateShowSerializer
        else:
            if not user.is_staff or not user.is_superuser:
                return ShowListSerializer
            return ShowSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateShowSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            mixin = CreateShowMixin(data=data)
            mixin.run()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


### SEATING VIEWS
class TheaterSeatingAPIView(generics.ListAPIView):
    queryset = TheaterSeating.objects.all()
    serializer_class = TheaterSeatingSerializer
    filterset_fields = ["theater", "booked"]


class TheaterSeatingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TheaterSeating.objects.all()
    serializer_class = TheaterSeatingSerializer

    lookup_field = "pk"
