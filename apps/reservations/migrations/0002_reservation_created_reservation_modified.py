# Generated by Django 5.0.7 on 2024-07-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="reservation",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]