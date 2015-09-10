# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0007_auto_20150825_1722'),
        ('students', '0004_tutorgroup_ophase'),
        ('staff', '0005_auto_20150825_1552'),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('spacing', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Ein Platz Abstand'), (2, 'Zwei Plätze Abstand')], verbose_name='Sitzplatzabstand')),
                ('mode', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Gleichmäßig auf alle Räume verteilen'), (1, 'Möglichst wenig Räume')], verbose_name='Verteilmodus')),
                ('group_category', models.ForeignKey(to='staff.GroupCategory', verbose_name='Gruppenkategorie')),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase')),
                ('selected_rooms', models.ManyToManyField(to='exam.ExamRoom')),
            ],
            options={
                'verbose_name_plural': 'Klausurzuteilungen',
                'verbose_name': 'Klausurzuteilung',
            },
        ),
        migrations.CreateModel(
            name='PersonToExamRoomAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('assignment', models.ForeignKey(to='exam.Assignment')),
                ('person', models.ForeignKey(to='students.Student')),
                ('room', models.ForeignKey(to='exam.ExamRoom')),
            ],
            options={
                'verbose_name_plural': 'Individuelle Klausurzuteilungen',
                'verbose_name': 'Individuelle Klausurzuteilung',
            },
        ),
    ]
