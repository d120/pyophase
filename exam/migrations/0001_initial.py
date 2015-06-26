# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoom',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('available', models.BooleanField(default=True, verbose_name='Verfügbar')),
                ('capacity_1_free', models.IntegerField(verbose_name='Plätze (1 Platz Abstand)')),
                ('capacity_2_free', models.IntegerField(verbose_name='Plätze (2 Plätze Abstand)')),
                ('room', models.OneToOneField(to='ophasebase.Room', verbose_name='Raum')),
            ],
            options={
                'ordering': ['available', '-capacity_1_free', '-capacity_2_free', 'room'],
                'verbose_name': 'Klausurraum',
                'verbose_name_plural': 'Klausurräume',
            },
        ),
    ]
