from django.contrib import admin
from apps.ticketing.models import Theater, TheaterSeating


# Register your models here.
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "number_of_seats"]


@admin.register(TheaterSeating)
class TheaterSeatAdmin(admin.ModelAdmin):
    list_display = ["id", "seating_date", "theater", "show", "seat_number", "booked"]
