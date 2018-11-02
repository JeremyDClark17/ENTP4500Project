# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-27 18:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UrTourn', '0024_remove_tournament_endtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 27, 18, 47, 12, 915759, tzinfo=utc)),
        ),
    ]