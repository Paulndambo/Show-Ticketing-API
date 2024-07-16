from django.shortcuts import render
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from apps.ticketing.models import Theater, TheaterSeating, Show
from apps.ticketing.serializers import (
    TheaterSerializer,
    TheaterSeatingSerializer,
    ShowSerializer,
    SeatingArrangementSerializer,
)
from apps.ticketing.methods.generate_seating import SeatingArrangementGenerator

from apps.core.custom_permissions import IsAdminOrReadOnly


# Create your views here.
class TheatreAPIView(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        theater = self.request.query_params.get("theater")
        specified_date = self.request.query_params.get("date")

        if theater and specified_date:
            search_date = datetime.strptime(specified_date, "%Y-%m-%d").date()
            # print(f"Theater: {theater}, String Date: {type(specified_date)}, Date: {type(search_date)}")
            seatings = TheaterSeating.objects.filter(seating_date=search_date).distinct(
                "theater"
            )
            print(seatings)

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


class ShowDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


### SEATING VIEWS
class GenerateSeatingArrangementAPIView(generics.CreateAPIView):
    serializer_class = SeatingArrangementSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                generator = SeatingArrangementGenerator(data=data)
                generator.generate_seating_arrangement()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TheaterSeatingAPIView(generics.ListAPIView):
    queryset = TheaterSeating.objects.all()
    serializer_class = TheaterSeatingSerializer
    filterset_fields = ["theater", "booked"]


class TheaterSeatingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TheaterSeating.objects.all()
    serializer_class = TheaterSeatingSerializer

    lookup_field = "pk"
