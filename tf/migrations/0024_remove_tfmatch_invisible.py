# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-24 10:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0023_player_tf_last_played'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tfmatch',
            name='invisible',
        ),
    ]