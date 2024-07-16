from rest_framework import serializers
from apps.ticketing.models import Theater, TheaterSeating, Show
from apps.reservations.serializers import ReservationSerializer


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = "__all__"


class ShowSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = "__all__"

    def get_reservations(self, obj):
        reservations = obj.showreservations.all()
        serializer = ReservationSerializer(instance=reservations, many=True)
        return serializer.data


class ShowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"


class CreateShowSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    theater = serializers.IntegerField()
    ticket_cost = serializers.DecimalField(max_digits=100, decimal_places=2)
    show_date = serializers.DateField()
    show_time = serializers.TimeField()
    seating_arrangement = serializers.JSONField()


class SeatingArrangementSerializer(serializers.Serializer):
    theater = serializers.IntegerField()
    show = serializers.IntegerField()
    number_of_rows = serializers.IntegerField()


class TheaterSeatingSerializer(serializers.ModelSerializer):
    theater_name = serializers.SerializerMethodField()
    show_title = serializers.SerializerMethodField()

    class Meta:
        model = TheaterSeating
        fields = "__all__"

    def get_theater_name(self, obj):
        return obj.theater.name if obj.theater else None

    def get_show_title(self, obj):
        return obj.show.title if obj.show else None
