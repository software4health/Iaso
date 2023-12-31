# Generated by Django 3.2.14 on 2022-08-04 08:43

from django.db import migrations


def create_entity_type_beneficiary(apps, schema_editor):
    Account = apps.get_model("iaso", "Account")
    accounts = Account.objects.all()
    EntityType = apps.get_model("iaso", "EntityType")
    for account in accounts:
        if not EntityType.objects.filter(name="Pregnant and lactating woman", account=account).exists():
            Data = apps.get_model("iaso", "EntityType")
            data = {"name": "Pregnant and lactating woman", "account": account}
            Data.objects.create(**data)
        if not EntityType.objects.filter(name="Children under 5", account=account).exists():
            Data = apps.get_model("iaso", "EntityType")
            data = {"name": "Children under 5", "account": account}
            Data.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0153_entitytype_account"),
    ]

    operations = [migrations.RunPython(create_entity_type_beneficiary)]
