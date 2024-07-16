# Generated by Django 5.0.7 on 2024-07-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0002_reservation_created_reservation_modified"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="reservation_type",
            field=models.CharField(
                choices=[
                    ("Single Ticket", "Single Ticket"),
                    ("Multi Ticket", "Multi Ticket"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
