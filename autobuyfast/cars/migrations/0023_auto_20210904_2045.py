# Generated by Django 3.1.13 on 2021-09-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0022_auto_20210904_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autosearch',
            name='car_year',
            field=models.CharField(blank=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default=2000, max_length=10, null=True, verbose_name='Car Manufacturing Year'),
        ),
    ]
