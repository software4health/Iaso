# Generated by Django 3.1.12 on 2021-10-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0031_merge_20211008_1509"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="obr_name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
