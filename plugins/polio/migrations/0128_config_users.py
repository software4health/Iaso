# Generated by Django 3.2.15 on 2023-04-20 09:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("polio", "0127_auto_20230414_0750"),
    ]

    operations = [
        migrations.AddField(
            model_name="config",
            name="users",
            field=models.ManyToManyField(blank=True, related_name="polioconfigs", to=settings.AUTH_USER_MODEL),
        ),
    ]
