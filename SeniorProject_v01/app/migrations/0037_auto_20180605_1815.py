# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_autofill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='Enter a description of the event.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_url',
            field=models.URLField(default='https://www.'),
        ),
    ]
