from django.contrib import admin
from apps.reservations.models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "show",
        "seat",
        "reservation_type",
        "ticket_cost",
        "status",
    ]
