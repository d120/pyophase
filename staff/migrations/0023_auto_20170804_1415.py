# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0022_auto_20170706_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nametag_long',
            field=models.TextField(blank=True, verbose_name='Langform'),
        ),
        migrations.AddField(
            model_name='person',
            name='nametag_shortname',
            field=models.CharField(blank=True, max_length=4, verbose_name='Kürzel (maximal 4 Zeichen)'),
        ),
    ]
