# Generated by Django 2.1.11 on 2020-06-15 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("iaso", "0053_auto_20200614_1556")]

    operations = [
        migrations.AddField(
            model_name="exportstatus", name="last_error_message", field=models.TextField(blank=True, null=True)
        )
    ]
