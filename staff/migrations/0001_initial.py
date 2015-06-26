# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DressSize',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='Kleidergröße', unique=True)),
                ('sort_key', models.PositiveSmallIntegerField(verbose_name='Position in Auflistung', unique=True)),
            ],
            options={
                'verbose_name_plural': 'Kleidergrößen',
                'verbose_name': 'Kleidergröße',
                'ordering': ['sort_key'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('prename', models.CharField(max_length=60, verbose_name='Vorname')),
                ('name', models.CharField(max_length=75, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail-Adresse')),
                ('phone', models.CharField(help_text='Deine Handynummer brauchen wir um dich schnell erreichen zu können.', verbose_name='Handynummer', max_length=30)),
                ('matriculated_since', models.CharField(help_text='Seit wann studierst du an der TU Darmstadt?', verbose_name='An der Uni seit', max_length=30)),
                ('degree_course', models.CharField(help_text='Bachelor, Master, Joint Bachelor of Arts, etc.', verbose_name='Aktuell angestrebter Abschluss', max_length=50)),
                ('experience_ophase', models.TextField(help_text='Wenn du schonmal bei einer Ophase geholfen hast, schreib uns wann das war und was du gemacht hast.', verbose_name='Bisherige Ophasenerfahrung')),
                ('why_participate', models.TextField(verbose_name='Warum möchtest du bei der Ophase mitmachen? ')),
                ('is_tutor', models.BooleanField(help_text='Möchtest du als Tutor bei der Ophase mitmachen?', default=False, verbose_name='Tutor')),
                ('is_orga', models.BooleanField(help_text='Möchtest du als Orga bei der Ophase mitmachen?', default=False, verbose_name='Orga')),
                ('is_helper', models.BooleanField(help_text='Möchtest du als Helfer bei der Ophase mitmachen?', default=False, verbose_name='Helfer')),
                ('remarks', models.TextField(help_text='Was sollten wir noch wissen?', verbose_name='Anmerkungen', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eingetragen am')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Verändert am')),
                ('dress_size', models.ForeignKey(to='staff.DressSize', help_text='Mitwirkende bekommen T-Shirts um sie besser zu erkennen. Damit dein T-Shirt passt brauchen wir deine Größe.', blank=True, null=True, verbose_name='Kleidergröße')),
                ('helper_jobs', models.ManyToManyField(to='ophasebase.HelperJob', help_text='Bei welchen Aufgaben kannst du dir vorstellen zu helfen?', verbose_name='Helferaufgaben', blank=True)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase')),
                ('orga_jobs', models.ManyToManyField(to='ophasebase.OrgaJob', help_text='Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?', verbose_name='Orgaaufgaben', blank=True)),
                ('tutor_for', models.ForeignKey(to='ophasebase.GroupCategory', help_text='Erstsemester welches Studiengangs möchtest du als Tutor betreuen?', blank=True, null=True, verbose_name='Tutor für')),
            ],
            options={
                'verbose_name_plural': 'Personen',
                'verbose_name': 'Person',
                'ordering': ['prename', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('tutor_registration_enabled', models.BooleanField(default=False, verbose_name='Tutor Registrierung aktiv')),
                ('orga_registration_enabled', models.BooleanField(default=False, verbose_name='Orga Registrierung aktiv')),
                ('helper_registration_enabled', models.BooleanField(default=False, verbose_name='Helfer Registrierung aktiv')),
            ],
            options={
                'verbose_name_plural': 'Einstellungen',
                'verbose_name': 'Einstellungen',
            },
        ),
        migrations.AlterUniqueTogether(
            name='dresssize',
            unique_together=set([('name', 'sort_key')]),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('ophase', 'prename', 'name', 'email')]),
        ),
    ]
