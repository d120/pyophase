# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 13:05
from __future__ import unicode_literals

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='image',
            field=models.ImageField(storage=website.models.OverwriteStorage(), upload_to=website.models.Schedule.fixedname_upload_to, verbose_name='Stundenplan Bild'),
        ),
    ]
