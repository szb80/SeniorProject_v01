# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-03 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20180602_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField(default=0)),
                ('minute', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='autofill',
        ),
        migrations.RemoveField(
            model_name='person',
            name='state_name',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
