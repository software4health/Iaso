# Generated by Django 3.2.15 on 2022-11-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0111_merge_20221110_1008"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="budget_current_state_key",
            field=models.CharField(default="-", max_length=100),
        ),
    ]
