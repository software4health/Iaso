# Generated by Django 3.0.7 on 2021-01-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("iaso", "0070_task")]

    operations = [
        migrations.RemoveField(model_name="task", name="finished"),
        migrations.AddField(
            model_name="task", name="name", field=models.TextField(default="task"), preserve_default=False
        ),
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("QUEUED", "Queued"),
                    ("RUNNING", "Running"),
                    ("EXPORTED", "Exported"),
                    ("ERRORED", "Errored"),
                    ("SKIPPED", "Skipped"),
                ],
                default="QUEUED",
                max_length=40,
            ),
        ),
    ]
