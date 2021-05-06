# Generated by Django 3.0.14 on 2021-05-05 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polio', '0003_auto_20210505_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='detection_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ONGOING', 'Ongoing'), ('FINISHED', 'Finished')], default='PENDING', max_length=10),
        ),
    ]
