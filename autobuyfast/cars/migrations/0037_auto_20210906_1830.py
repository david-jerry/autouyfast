# Generated by Django 3.1.13 on 2021-09-06 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0036_auto_20210906_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img_url',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Alternative Image Upload Field'),
        ),
    ]
