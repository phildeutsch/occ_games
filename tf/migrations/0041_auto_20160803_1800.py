# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-03 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0040_match_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='fifamatch',
            name='matchtype',
            field=models.CharField(default='FF', max_length=2),
        ),
        migrations.AddField(
            model_name='tfmatch',
            name='matchtype',
            field=models.CharField(default='TF', max_length=2),
        ),
        migrations.AlterField(
            model_name='match',
            name='season',
            field=models.IntegerField(default=1),
        ),
    ]
