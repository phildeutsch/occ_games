# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-01 14:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0011_auto_20160609_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tfteam',
            name='team_elo',
        ),
    ]
