from rest_framework import serializers
from apps.ticketing.models import Theater, TheaterSeating, Show


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = "__all__"


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"


class SeatingArrangementSerializer(serializers.Serializer):
    theater = serializers.IntegerField()
    show = serializers.IntegerField()
    number_of_rows = serializers.IntegerField()


class TheaterSeatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterSeating
        fields = "__all__"
