# Generated by Django 5.0.7 on 2024-07-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Theatre",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("location", models.JSONField(null=True)),
                ("location_description", models.CharField(max_length=255)),
                ("town", models.CharField(max_length=255)),
                ("number_of_seats", models.IntegerField(default=1)),
                ("number_of_screens", models.IntegerField(default=1)),
                ("opened_on", models.DateField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]