# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
        ('ophasebase', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('spacing', models.PositiveSmallIntegerField(verbose_name='Sitzplatzabstand', choices=[(1, 'Ein Platz Abstand'), (2, 'Zwei Plätze Abstand')], default=2)),
                ('mode', models.PositiveSmallIntegerField(verbose_name='Verteilmodus', choices=[(0, 'Gleichmäßig auf alle Räume verteilen'), (1, 'Möglichst wenig Räume')], default=0)),
                ('count', models.PositiveIntegerField(verbose_name='# Zuteilungen')),
                ('group_category', models.ForeignKey(verbose_name='Gruppenkategorie', to='staff.GroupCategory', on_delete=models.CASCADE)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Klausurzuteilung',
                'verbose_name_plural': 'Klausurzuteilungen',
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='ExamRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available', models.BooleanField(verbose_name='Verfügbar', default=True)),
                ('capacity_1_free', models.IntegerField(verbose_name='Plätze (1 Platz Abstand)')),
                ('capacity_2_free', models.IntegerField(verbose_name='Plätze (2 Plätze Abstand)')),
                ('room', models.OneToOneField(to='ophasebase.Room', verbose_name='Raum', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Klausurraum',
                'verbose_name_plural': 'Klausurräume',
                'ordering': ['available', '-capacity_1_free', '-capacity_2_free', 'room'],
            },
        ),
        migrations.CreateModel(
            name='PersonToExamRoomAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment', models.ForeignKey(to='exam.Assignment', on_delete=models.CASCADE)),
                ('person', models.ForeignKey(to='students.Student', on_delete=models.CASCADE)),
                ('room', models.ForeignKey(to='exam.ExamRoom', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Individuelle Klausurzuteilung',
                'verbose_name_plural': 'Individuelle Klausurzuteilungen',
                'ordering': ['assignment', 'room', 'person__name', 'person__prename'],
            },
        ),
    ]
