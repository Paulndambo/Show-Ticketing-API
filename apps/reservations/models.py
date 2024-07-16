from django.db import models

# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    show = models.ForeignKey("ticketing.Show", on_delete=models.PROTECT)
    seat = models.OneToOneField("ticketing.TheaterSeating", on_delete=models.PROTECT)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)