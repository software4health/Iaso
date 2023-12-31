# Generated by Django 3.2.15 on 2023-06-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0135_alter_rounddatehistoryentry_reason"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="payment_mode",
            field=models.CharField(
                blank=True,
                choices=[("DIRECT", "Direct"), ("DFC", "DFC"), ("MOBILE_PAYMENT", "Mobile Payment")],
                max_length=30,
                null=True,
            ),
        ),
    ]
