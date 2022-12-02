# Generated by Django 3.2.15 on 2022-12-02 12:08

# We will (in the next migration) make the StorageDevice.status_updated_at field non-nullable for long-term robustness
# (see https://bluesquare.atlassian.net/browse/WC2-115). To make sure this upcoming migration will succeed, we need to
# make sure all existing StorageDevice objects have a non-null status_updated_at field. This migration will solve that
# problem

from django.db import migrations


def populate_status_updated_at(apps, schema_editor):
    StorageDevice = apps.get_model("iaso", "StorageDevice")
    for device in StorageDevice.objects.all():
        if device.status_updated_at is None:
            log_for_status_changes = device.log_entries.filter(operation_type="CHANGE_STATUS")
            if log_for_status_changes:
                # We have log entries for status changes, we can use the timestamp of the most recent one
                last_status_change_log = log_for_status_changes.order_by("-performed_at").first()
                device.status_updated_at = last_status_change_log.performed_at
            else:
                # No log entries for status changes, we use the device creation time
                device.status_updated_at = device.created_at
            device.save()


class Migration(migrations.Migration):

    dependencies = [
        ("iaso", "0178_remove_beneficiary_user_perm"),
    ]

    operations = [
        migrations.RunPython(populate_status_updated_at, migrations.RunPython.noop),
    ]
