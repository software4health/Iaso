# Generated by Django 3.2.21 on 2023-09-21 15:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0233_migrate_data_to_reference_forms_and_reference_instances"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orgunit",
            name="reference_instance",
        ),
        migrations.RemoveField(
            model_name="orgunittype",
            name="reference_form",
        ),
    ]
