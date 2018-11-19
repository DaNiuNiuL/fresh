# Generated by Django 2.1.1 on 2018-10-09 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_auto_20180930_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='image',
            field=models.CharField(default='/static/images/banner01.jpg', max_length=100, verbose_name='分类的展示图片'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 9, 15, 30, 53, 790101), verbose_name='创建时间'),
        ),
    ]