# Generated by Django 3.2.15 on 2023-06-22 16:18

from django.db import migrations


def create_feature_flags(apps, schema_editor):
    FeatureFlag = apps.get_model("iaso", "FeatureFlag")
    FeatureFlag.objects.create(
        code="MOBILE_FORCE_FORMS_UPDATE",
        name="Mobile: Warn the user when forms have been updated and force them to update.",
    )


def destroy_feature_flags(apps, schema_editor):
    FeatureFlag = apps.get_model("iaso", "FeatureFlag")
    FeatureFlag.objects.filter(code="MOBILE_FORCE_FORMS_UPDATE").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0218_add_feature_flag_MOBILE_CHECK_OU_UPDATE"),
    ]

    operations = [migrations.RunPython(create_feature_flags, destroy_feature_flags)]
