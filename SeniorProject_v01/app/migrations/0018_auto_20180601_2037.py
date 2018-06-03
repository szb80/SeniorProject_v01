# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-02 03:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_auto_20180601_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creation_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]