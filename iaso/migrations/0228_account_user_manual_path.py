# Generated by Django 3.2.15 on 2023-08-28 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0227_add_account_feature_flag_SHOW_BENEFICIARY_TYPES_IN_LIST_MENU"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="user_manual_path",
            field=models.TextField(blank=True, null=True),
        ),
    ]
