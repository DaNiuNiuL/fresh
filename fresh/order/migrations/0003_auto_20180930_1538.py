# Generated by Django 2.1.1 on 2018-09-30 07:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180929_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 30, 15, 38, 27, 587785), verbose_name='创建时间'),
        ),
    ]
