# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
        ('ophasebase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('student_registration_enabled', models.BooleanField(default=False, verbose_name='Klausuranmeldung aktiv')),
            ],
            options={
                'verbose_name_plural': 'Einstellungen',
                'verbose_name': 'Einstellungen',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('prename', models.CharField(max_length=50, verbose_name='Vorname')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='E-Mail-Adresse')),
                ('wantExam', models.BooleanField(default=False, verbose_name='Klausur mitschreiben?')),
                ('wantNewsletter', models.BooleanField(default=False, verbose_name='Newsletter abonnieren?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase')),
            ],
            options={
                'verbose_name_plural': 'Ersties',
                'ordering': ['tutorGroup', 'name', 'prename'],
                'verbose_name': 'Erstie',
            },
        ),
        migrations.CreateModel(
            name='TutorGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Gruppenname')),
                ('groupCategory', models.ForeignKey(to='ophasebase.GroupCategory', verbose_name='Gruppenkategorie')),
                ('tutors', models.ManyToManyField(to='staff.Person', verbose_name='Tutoren')),
            ],
            options={
                'verbose_name_plural': 'Kleingruppen',
                'ordering': ['groupCategory', 'name'],
                'verbose_name': 'Kleingruppe',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='tutorGroup',
            field=models.ForeignKey(to='students.TutorGroup', verbose_name='Kleingruppe'),
        ),
    ]
