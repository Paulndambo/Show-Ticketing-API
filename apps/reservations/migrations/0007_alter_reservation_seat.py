# Generated by Django 5.0.7 on 2024-07-16 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0006_reservation_notification_send_reservation_status"),
        ("ticketing", "0013_alter_theater_created_alter_theater_modified_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="seat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="ticketing.theaterseating",
            ),
        ),
    ]
