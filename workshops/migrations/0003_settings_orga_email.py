# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0002_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='orga_email',
            field=models.CharField(default='workshops@example.org', max_length=100, verbose_name='E-Mail-Adresse des Workshop-Orgas'),
            preserve_default=False,
        ),
    ]
