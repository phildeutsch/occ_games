# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-21 14:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0018_auto_20160709_0851'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TfPlayer',
            new_name='Player',
        ),
    ]
