# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-23 20:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0021_auto_20160722_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='matches_played',
            new_name='tf_matches_played',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='matches_won',
            new_name='tf_matches_won',
        ),
    ]
