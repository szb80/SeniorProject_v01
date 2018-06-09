# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 05:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20180606_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time_start',
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
