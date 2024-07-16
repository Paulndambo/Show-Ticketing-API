from rest_framework import serializers
from apps.reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    seat_number = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = "__all__"

    def get_customer_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_seat_number(self, obj):
        return obj.seat.seat_number


class ReserveSeatSerializer(serializers.Serializer):
    seats = serializers.JSONField()
    show = serializers.IntegerField()
    ticket_cost = serializers.DecimalField(max_digits=100, decimal_places=2)


class CancelReservationSerializer(serializers.Serializer):
    seats = serializers.JSONField()
