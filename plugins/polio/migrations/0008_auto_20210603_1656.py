# Generated by Django 3.0.14 on 2021-06-03 16:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0007_merge_20210602_1615"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="gpei_coordinator",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="campaign",
            name="payment_mode",
            field=models.CharField(
                blank=True, choices=[("DIRECT", "Direct"), ("DFC", "DFC")], max_length=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="campaign",
            name="verification_score",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
