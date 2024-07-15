from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from apps.ticketing.models import Theater
from apps.ticketing.serializers import TheaterSerializer
from apps.ticketing.mixins.create_theater import TheaterMixin


# Create your views here.
class TheatreAPIView(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                mixin = TheaterMixin(data=data)
                mixin.onboard_theater()
                return Response(
                    {"message": "Theater successfully created"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)


class TheaterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    lookup_field = "pk"

