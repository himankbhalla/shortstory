# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-13 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Story', '0010_auto_20160612_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='scribble',
            name='is_poem',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scribble',
            name='is_quote',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scribble',
            name='is_shtory',
            field=models.BooleanField(default=True),
        ),
    ]
