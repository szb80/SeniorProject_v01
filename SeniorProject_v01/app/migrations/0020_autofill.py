# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-02 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_merge_20180601_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='autofill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=400)),
            ],
        ),
    ]
