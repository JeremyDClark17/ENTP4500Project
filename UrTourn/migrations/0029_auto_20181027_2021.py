# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-27 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UrTourn', '0028_auto_20181027_2009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='startDay',
            new_name='start_day',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='startTime',
            new_name='start_time',
        ),
    ]
