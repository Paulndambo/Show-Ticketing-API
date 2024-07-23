from django.shortcuts import render
from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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
@method_decorator(cache_page(60*5), name='dispatch')
class TheatreAPIView(generics.ListCreateAPIView):
    queryset = Theater.objects.all().order_by("-created")
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
            queryset = self.queryset.exclude(id__in=seatings)
        else:
            queryset = super().get_queryset()

        return queryset
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache_key = "theaters_list"
        cache.delete(cache_key)


class TheaterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all().order_by("-created")
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

    lookup_field = "pk"


## Shows views
@method_decorator(cache_page(60*5), name='dispatch')
class ShowsAPIView(generics.ListCreateAPIView):
    queryset = Show.objects.all().order_by("-created")
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


    def get_queryset(self):
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateShowSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            mixin = CreateShowMixin(data=data)
            mixin.run()
            cache.delete("shows_list")  # Clear cache after creating new show
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
