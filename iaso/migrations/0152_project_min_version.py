# Generated by Django 3.2.14 on 2022-07-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0151_auto_20220718_1013"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="min_version",
            field=models.IntegerField(null=True),
        ),
    ]
