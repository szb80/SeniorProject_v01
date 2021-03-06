# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 01:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='John', max_length=255)),
                ('last_name', models.TextField(default='Doe', max_length=255)),
                ('email', models.EmailField(default='contact@me.co', max_length=254)),
                ('street_address', models.TextField(default='')),
                ('postal_code', models.IntegerField(default=0)),
                ('city', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='state_ID',
        ),
        migrations.RemoveField(
            model_name='user',
            name='troop_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_level',
        ),
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='type_name',
        ),
        migrations.RemoveField(
            model_name='troop',
            name='district_ID',
        ),
        migrations.AddField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='event',
            name='street_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='eventtype',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='district_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='pointman_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='descrption',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_link',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='primary_contact_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
        migrations.AlterField(
            model_name='event',
            name='zipcode',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='region',
            name='region_name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='state',
            name='abbreviation',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='state',
            name='state_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='UserLevel',
        ),
        migrations.AddField(
            model_name='person',
            name='state_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.State'),
        ),
        migrations.AddField(
            model_name='person',
            name='troop_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Troop'),
        ),
    ]
