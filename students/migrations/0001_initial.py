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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_registration_enabled', models.BooleanField(verbose_name='Klausuranmeldung aktiv', default=False)),
            ],
            options={
                'verbose_name': 'Einstellungen',
                'verbose_name_plural': 'Einstellungen',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prename', models.CharField(verbose_name='Vorname', max_length=50)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('email', models.EmailField(verbose_name='E-Mail-Adresse', max_length=254, blank=True)),
                ('want_exam', models.BooleanField(verbose_name='Klausur mitschreiben?', default=False)),
                ('want_newsletter', models.BooleanField(verbose_name='Newsletter abonnieren?', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Erstie',
                'verbose_name_plural': 'Ersties',
                'ordering': ['tutor_group', 'name', 'prename'],
            },
        ),
        migrations.CreateModel(
            name='TutorGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Gruppenname', max_length=50)),
                ('group_category', models.ForeignKey(verbose_name='Gruppenkategorie', to='staff.GroupCategory', on_delete=models.CASCADE)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase', on_delete=models.CASCADE)),
                ('tutors', models.ManyToManyField(verbose_name='Tutoren', to='staff.Person')),
            ],
            options={
                'verbose_name': 'Kleingruppe',
                'verbose_name_plural': 'Kleingruppen',
                'ordering': ['group_category', 'name'],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='tutor_group',
            field=models.ForeignKey(verbose_name='Kleingruppe', to='students.TutorGroup', on_delete=models.CASCADE),
        ),
    ]
