# Generated by Django 2.1.11 on 2020-05-24 11:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("iaso", "0048_merge_20200522_1405")]

    operations = [migrations.RemoveField(model_name="groupset", name="projects")]
