# Generated by Django 5.0.7 on 2024-07-16 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticketing", "0014_alter_show_theater"),
    ]

    operations = [
        migrations.RenameField(
            model_name="show",
            old_name="date",
            new_name="show_date",
        ),
    ]
