# Generated by Django 2.1.1 on 2018-10-10 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20181010_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 10, 15, 18, 12, 991522), verbose_name='创建时间'),
        ),
    ]