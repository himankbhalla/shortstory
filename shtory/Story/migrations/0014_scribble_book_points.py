# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-24 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Story', '0013_scribble_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='scribble',
            name='book_points',
            field=models.IntegerField(default=0),
        ),
    ]
