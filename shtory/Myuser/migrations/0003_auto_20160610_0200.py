# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-10 02:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myuser', '0002_auto_20160609_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(through='Myuser.Relationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 6, 10)),
        ),
    ]
