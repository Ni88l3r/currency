# Generated by Django 2.2.12 on 2020-06-07 14:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0002_auto_20200607_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 7, 14, 30, 3, 96827, tzinfo=utc)),
        ),
    ]