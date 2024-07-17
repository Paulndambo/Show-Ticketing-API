from django.shortcuts import render
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime
from django.core.cache import cache


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
from apps.core.custom_pagination import NoPagination


# Create your views here.
class TheatreAPIView(generics.ListCreateAPIView):
    queryset = Theater.objects.all().order_by("-created")
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]
 
    def get_queryset(self):
        specified_date = self.request.query_params.get("date")
        cache_key = f'theater_list_{specified_date}' if specified_date else 'theater_list_all'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        if specified_date:
            search_date = datetime.strptime(specified_date, "%Y-%m-%d").date()
            seatings = (
                TheaterSeating.objects.filter(seating_date=search_date)
                .values_list("theater_id", flat=True)
                .distinct()
            )
            queryset = self.queryset.exclude(id__in=seatings)
        else:
            queryset = super().get_queryset()

        cache.set(cache_key, queryset, timeout=60*15)  # Cache for 15 minutes
        return queryset
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.clear()  # Clear cache on create

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.clear()  # Clear cache on update


class TheaterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all().order_by("-created")
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


## Shows views
class ShowsAPIView(generics.ListCreateAPIView):
    queryset = Show.objects.all().order_by("-created")
    serializer_class = ShowSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = NoPagination
    cache_key = 'shows_list'

    def get_serializer_class(self, *args, **kwargs):
        user = self.request.user
        if self.request.method in ["POST", "post"]:
            return CreateShowSerializer
        else:
            if not user.is_staff or not user.is_superuser:
                return ShowListSerializer
            return ShowSerializer
        
    def get_queryset(self):
        cached_shows = cache.get(self.cache_key)
        if cached_shows is None:
            cached_shows = super().get_queryset()
            cache.set(self.cache_key, cached_shows, timeout=60*15)  # Cache timeout of 15 minutes
        return cached_shows

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateShowSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            mixin = CreateShowMixin(data=data)
            mixin.run()
            cache.delete('shows_list')  # Invalidate cache on post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all().order_by("-created")
    serializer_class = ShowSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


### SEATING VIEWS
class TheaterSeatingAPIView(generics.ListAPIView):
    queryset = TheaterSeating.objects.all().order_by("-created")
    serializer_class = TheaterSeatingSerializer
    filterset_fields = ["theater", "booked"]
    permission_classes = [IsAdminOrReadOnly]


class TheaterSeatingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TheaterSeating.objects.all().order_by("-created")
    serializer_class = TheaterSeatingSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"
