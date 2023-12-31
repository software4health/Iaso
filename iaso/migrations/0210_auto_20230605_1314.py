# Generated by Django 3.2.15 on 2023-06-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0209_merge_20230605_1312"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entityduplicate",
            name="metadata",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="entityduplicateanalyze",
            name="algorithm",
            field=models.CharField(choices=[["levenshtein", "levenshtein"]], default="levenshtein", max_length=20),
        ),
    ]
