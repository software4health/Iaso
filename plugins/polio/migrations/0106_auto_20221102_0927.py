# Generated by Django 3.2.15 on 2022-11-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polio', '0105_merge_20221021_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='forma_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='forma_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
