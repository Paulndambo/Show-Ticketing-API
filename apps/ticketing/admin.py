from django.contrib import admin
from apps.ticketing.models import Theater, TheaterSeat

# Register your models here.
admin.site.register(Theater)


@admin.register(TheaterSeat)
class TheaterSeatAdmin(admin.ModelAdmin):
    list_display = ["id", "theater", "seat_number", "booked"]
