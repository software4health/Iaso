# Generated by Django 3.2.15 on 2023-04-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0197_formpredefinedfilter"),
    ]

    operations = [
        migrations.AddField(
            model_name="formversion",
            name="possible_fields",
            field=models.JSONField(
                blank=True,
                editable=False,
                help_text="Questions present in this form version, as a flat list.Update on save. See equivalent on Form for all version",
                null=True,
            ),
        ),
    ]
