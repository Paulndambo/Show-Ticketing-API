# Generated by Django 5.0.7 on 2024-07-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0008_alter_reservation_show_alter_reservation_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
