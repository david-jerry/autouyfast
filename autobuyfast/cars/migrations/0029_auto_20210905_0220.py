# Generated by Django 3.1.13 on 2021-09-05 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0028_auto_20210905_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autosearch',
            name='dealer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='autosearch',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Car Title'),
        ),
    ]
