# Generated by Django 3.0.14 on 2021-05-19 09:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("polio", "0004_auto_20210505_1813"),
    ]

    operations = [
        migrations.CreateModel(
            name="Preparedness",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "planning_score",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Planning, coordination and funding"
                    ),
                ),
                (
                    "training_score",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Training for SIAs quality"),
                ),
                (
                    "monitoring_score",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Monitoring and Supervision"),
                ),
                (
                    "vaccine_score",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Vaccine, cold chain and logistics"
                    ),
                ),
                (
                    "advocacy_score",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Advocacy, social mobilization and communication"
                    ),
                ),
                (
                    "adverse_score",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Adverse Event Following Immunization (AEFI)"
                    ),
                ),
                (
                    "status_score",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Status of preparedness"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="campaign",
            name="spreadsheet_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="campaign",
            name="preperadness_national_score",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="polio.Preparedness"
            ),
        ),
    ]
