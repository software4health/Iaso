# Generated by Django 3.1.12 on 2021-07-01 20:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0015_auto_20210630_2051"),
    ]

    operations = [
        migrations.CreateModel(
            name="Config",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("content", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
