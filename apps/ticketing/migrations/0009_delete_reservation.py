# Generated by Django 5.0.7 on 2024-07-16 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticketing", "0008_rename_charge_per_person_show_ticket_cost"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Reservation",
        ),
    ]
