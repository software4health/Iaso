# Generated by Django 3.2.15 on 2023-03-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0124_merge_20230316_1049"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="re_submitted_to_orpg_operations1_at_WFEDITABLE",
            field=models.DateField(blank=True, null=True),
        ),
    ]
