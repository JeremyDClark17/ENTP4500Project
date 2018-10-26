# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-25 00:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UrTourn', '0012_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='id',
        ),
        migrations.AddField(
            model_name='tournament',
            name='tournament_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
