# Generated by Django 2.2.4 on 2019-08-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("vector_control", "0028_auto_20190628_1342")]

    operations = [
        migrations.AddField(
            model_name="apiimport",
            name="has_problem",
            field=models.BooleanField(default=False),
        )
    ]
