# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-05 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0024_tutorgroup_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='tuid',
            field=models.BooleanField(null=True, default=True, verbose_name='TUID User'),
        ),
    ]
