# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-05 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0024_tutorgroup_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='tuid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyTUID.TUIDUser', verbose_name='TUID User'),
        ),
    ]
