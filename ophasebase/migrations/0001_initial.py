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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('area', models.CharField(verbose_name='Campus', max_length=1, default='S', choices=[('B', 'Botanischer Garten (B)'), ('H', 'Hochschulstadion (H)'), ('L', 'Lichtwiese (L)'), ('S', 'Stadtmitte (S)'), ('W', 'Windkanal (W)')])),
                ('subarea', models.PositiveSmallIntegerField(verbose_name='Campusabschnitt')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Gebäudenummer')),
                ('label', models.CharField(blank=True, verbose_name='Gebäudename', max_length=50, default='')),
                ('remarks', models.CharField(blank=True, verbose_name='Anmerkungen', max_length=200, default='')),
            ],
            options={
                'ordering': ['area', 'subarea', 'number'],
                'verbose_name': 'Gebäude',
                'verbose_name_plural': 'Gebäude',
            },
        ),
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('label', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Gruppenkategorie',
                'verbose_name_plural': 'Gruppenkategorien',
            },
        ),
        migrations.CreateModel(
            name='HelperJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('has_enough_persons', models.BooleanField(verbose_name='Ausreichend Personen', help_text='Sind bereits ausreichend Personen für den Job vorhanden?', default=False)),
            ],
            options={
                'verbose_name': 'Helferjob',
                'verbose_name_plural': 'Helferjobs',
            },
        ),
        migrations.CreateModel(
            name='Ophase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_date', models.DateField(verbose_name='Beginn')),
                ('end_date', models.DateField(verbose_name='Ende')),
                ('is_active', models.BooleanField(verbose_name='Aktiv?', default=False)),
                ('group_categories', models.ManyToManyField(verbose_name='Kleingruppenkategorien', to='ophasebase.GroupCategory')),
                ('helper_jobs', models.ManyToManyField(verbose_name='Helferjobs', to='ophasebase.HelperJob')),
            ],
            options={
                'verbose_name': 'Ophase',
                'verbose_name_plural': 'Ophasen',
            },
        ),
        migrations.CreateModel(
            name='OrgaJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('has_enough_persons', models.BooleanField(verbose_name='Ausreichend Personen', help_text='Sind bereits ausreichend Personen für den Job vorhanden?', default=False)),
            ],
            options={
                'verbose_name': 'Orgajob',
                'verbose_name_plural': 'Orgajobs',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.CharField(verbose_name='Nummer', max_length=50)),
                ('type', models.CharField(verbose_name='Typ', max_length=2, choices=[('SR', 'Kleingruppenraum'), ('HS', 'Hörsaal'), ('PC', 'PC-Pool'), ('LZ', 'Lernzentrum'), ('SO', 'Sonstiges')])),
                ('hasBeamer', models.BooleanField(verbose_name='Beamer vorhanden?', default=False)),
                ('capacity', models.IntegerField(verbose_name='Anzahl Plätze')),
                ('lat', models.FloatField(blank=True, verbose_name='Latitude', default=0)),
                ('lng', models.FloatField(blank=True, verbose_name='Longitude', default=0)),
                ('building', models.ForeignKey(verbose_name='Gebäude', to='ophasebase.Building')),
            ],
            options={
                'ordering': ['building', 'number'],
                'verbose_name': 'Raum',
                'verbose_name_plural': 'Räume',
            },
        ),
        migrations.AddField(
            model_name='ophase',
            name='orga_jobs',
            field=models.ManyToManyField(verbose_name='Orgajobs', to='ophasebase.OrgaJob'),
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
