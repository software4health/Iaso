# Generated by Django 3.0.7 on 2021-03-12 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0081_instance_to_export"),
    ]

    operations = [
        migrations.AddField(
            model_name="exportrequest",
            name="continue_on_error",
            field=models.BooleanField(default=False),
        ),
    ]
