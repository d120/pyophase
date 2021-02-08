# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyTUID', '0003_auto_20170514_1146'),
        ('ophasebase', '0007_auto_20170215_1416'),
        ('staff', '0018_person_tutor_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='tuid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pyTUID.TUIDUser', verbose_name='TUID User'),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('ophase', 'email'), ('ophase', 'tuid')]),
        ),
    ]
