# Generated by Django 3.1.13 on 2021-09-08 04:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_auto_20210908_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrequest',
            name='pickup',
            field=models.DateField(default=datetime.datetime(2021, 9, 8, 4, 2, 36, 168128, tzinfo=utc), null=True, verbose_name='Pickup Date'),
        ),
    ]
