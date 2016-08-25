# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.CharField(verbose_name='Campus', max_length=1, choices=[('B', 'Botanischer Garten (B)'), ('H', 'Hochschulstadion (H)'), ('L', 'Lichtwiese (L)'), ('S', 'Stadtmitte (S)'), ('W', 'Windkanal (W)')], default='S')),
                ('subarea', models.PositiveSmallIntegerField(verbose_name='Campusabschnitt')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Gebäudenummer')),
                ('label', models.CharField(verbose_name='Gebäudename', max_length=50, blank=True, default='')),
                ('remarks', models.CharField(verbose_name='Anmerkungen', max_length=200, blank=True, default='')),
            ],
            options={
                'verbose_name': 'Gebäude',
                'verbose_name_plural': 'Gebäude',
                'ordering': ['area', 'subarea', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Ophase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(verbose_name='Beginn')),
                ('end_date', models.DateField(verbose_name='Ende')),
                ('is_active', models.BooleanField(verbose_name='Aktiv?', default=False)),
            ],
            options={
                'verbose_name': 'Ophase',
                'verbose_name_plural': 'Ophasen',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(verbose_name='Nummer', max_length=50)),
                ('type', models.CharField(verbose_name='Typ', max_length=2, choices=[('SR', 'Kleingruppenraum'), ('HS', 'Hörsaal'), ('PC', 'PC-Pool'), ('LZ', 'Lernzentrum'), ('SO', 'Sonstiges')])),
                ('has_beamer', models.BooleanField(verbose_name='Beamer vorhanden?', default=False)),
                ('capacity', models.IntegerField(verbose_name='Anzahl Plätze')),
                ('lat', models.FloatField(verbose_name='Latitude', blank=True, default=0)),
                ('lng', models.FloatField(verbose_name='Longitude', blank=True, default=0)),
                ('building', models.ForeignKey(verbose_name='Gebäude', to='ophasebase.Building', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Raum',
                'verbose_name_plural': 'Räume',
                'ordering': ['building', 'number'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='building',
            unique_together=set([('area', 'subarea', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('building', 'number')]),
        ),
    ]
