# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-17 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UrTourn', '0004_auto_20181017_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]