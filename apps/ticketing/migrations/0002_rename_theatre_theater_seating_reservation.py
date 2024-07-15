# Generated by Django 5.0.7 on 2024-07-15 17:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticketing", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Theatre",
            new_name="Theater",
        ),
        migrations.CreateModel(
            name="Seating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("show_time", models.TimeField()),
                (
                    "theater",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ticketing.theater",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seat_number", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "seating",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ticketing.seating",
                    ),
                ),
            ],
        ),
    ]
