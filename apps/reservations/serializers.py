from rest_framework import serializers
from apps.reservations.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class ReserveSeatSerializer(serializers.Serializer):
    customer = serializers.IntegerField()
    seat = serializers.IntegerField()
    show = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=100, decimal_places=2)