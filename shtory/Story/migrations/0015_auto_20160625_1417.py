# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-25 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Story', '0014_scribble_book_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scribble',
            name='story',
            field=models.TextField(max_length=1200),
        ),
    ]
