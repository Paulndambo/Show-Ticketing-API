# Generated by Django 5.0.7 on 2024-07-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_created_alter_user_modified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]