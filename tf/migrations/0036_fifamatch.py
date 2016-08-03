# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-31 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0035_auto_20160731_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='FifaMatch',
            fields=[
                ('match_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tf.Match')),
            ],
            options={
                'verbose_name_plural': 'fifa matches',
            },
            bases=('tf.match',),
        ),
    ]