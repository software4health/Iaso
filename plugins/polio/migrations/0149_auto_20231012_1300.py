# Generated by Django 3.2.21 on 2023-10-12 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polio', '0148_merge_20231002_1610'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roundvaccine',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='roundvaccine',
            name='round',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='round',
        ),
        migrations.DeleteModel(
            name='Destruction',
        ),
        migrations.DeleteModel(
            name='RoundVaccine',
        ),
        migrations.DeleteModel(
            name='Shipment',
        ),
    ]
