# Generated by Django 5.0.7 on 2024-07-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticketing", "0012_alter_theater_created_alter_theater_modified_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theater",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="theater",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="theaterseating",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="theaterseating",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]