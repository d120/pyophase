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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Kleidergröße', unique=True, max_length=75)),
                ('sort_key', models.PositiveSmallIntegerField(verbose_name='Position in Auflistung', unique=True)),
            ],
            options={
                'verbose_name': 'Kleidergröße',
                'verbose_name_plural': 'Kleidergrößen',
                'ordering': ['sort_key'],
            },
        ),
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Helferjob',
                'verbose_name_plural': 'Helferjobs',
            },
        ),
        migrations.CreateModel(
            name='OrgaJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Orgajob',
                'verbose_name_plural': 'Orgajobs',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prename', models.CharField(verbose_name='Vorname', max_length=60)),
                ('name', models.CharField(verbose_name='Name', max_length=75)),
                ('email', models.EmailField(verbose_name='E-Mail-Adresse', max_length=254)),
                ('phone', models.CharField(verbose_name='Handynummer', max_length=30, help_text='Deine Handynummer brauchen wir um dich schnell erreichen zu können.')),
                ('matriculated_since', models.CharField(verbose_name='An der Uni seit', max_length=30, help_text='Seit wann studierst du an der TU Darmstadt?')),
                ('degree_course', models.CharField(verbose_name='Aktuell angestrebter Abschluss', max_length=50, help_text='Bachelor, Master, Joint Bachelor of Arts, etc.')),
                ('experience_ophase', models.TextField(verbose_name='Bisherige Ophasenerfahrung', help_text='Wenn du schonmal bei einer Ophase geholfen hast, schreib uns wann das war und was du gemacht hast.')),
                ('why_participate', models.TextField(verbose_name='Warum möchtest du bei der Ophase mitmachen? ')),
                ('is_tutor', models.BooleanField(verbose_name='Tutor', default=False, help_text='Möchtest du als Tutor bei der Ophase mitmachen?')),
                ('is_orga', models.BooleanField(verbose_name='Orga', default=False, help_text='Möchtest du als Orga bei der Ophase mitmachen?')),
                ('is_helper', models.BooleanField(verbose_name='Helfer', default=False, help_text='Möchtest du als Helfer bei der Ophase mitmachen?')),
                ('remarks', models.TextField(verbose_name='Anmerkungen', blank=True, help_text='Was sollten wir noch wissen?')),
                ('created_at', models.DateTimeField(verbose_name='Eingetragen am', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Verändert am', auto_now=True)),
                ('dress_size', models.ForeignKey(to='staff.DressSize', null=True, help_text='Mitwirkende bekommen T-Shirts um sie besser zu erkennen. Damit dein T-Shirt passt brauchen wir deine Größe.', verbose_name='Kleidergröße', blank=True, on_delete=models.SET_NULL)),
                ('helper_jobs', models.ManyToManyField(verbose_name='Helferaufgaben', to='staff.HelperJob', blank=True, help_text='Bei welchen Aufgaben kannst du dir vorstellen zu helfen?')),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase', on_delete=models.CASCADE)),
                ('orga_jobs', models.ManyToManyField(verbose_name='Orgaaufgaben', to='staff.OrgaJob', blank=True, help_text='Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?')),
                ('tutor_for', models.ForeignKey(to='staff.GroupCategory', null=True, help_text='Erstsemester welches Studiengangs möchtest du als Tutor betreuen?', verbose_name='Tutor für', blank=True, on_delete=models.SET_NULL)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personen',
                'ordering': ['prename', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tutor_registration_enabled', models.BooleanField(verbose_name='Tutor Registrierung aktiv', default=False)),
                ('orga_registration_enabled', models.BooleanField(verbose_name='Orga Registrierung aktiv', default=False)),
                ('helper_registration_enabled', models.BooleanField(verbose_name='Helfer Registrierung aktiv', default=False)),
                ('group_categories_enabled', models.ManyToManyField(verbose_name='Freigeschaltete Kleingruppenkategorien', to='staff.GroupCategory')),
                ('helper_jobs_enabled', models.ManyToManyField(verbose_name='Freigeschaltete Helferjobs', to='staff.HelperJob')),
                ('orga_jobs_enabled', models.ManyToManyField(verbose_name='Freigeschaltete Orgajobs', to='staff.OrgaJob')),
            ],
            options={
                'verbose_name': 'Einstellungen',
                'verbose_name_plural': 'Einstellungen',
            },
        ),
        migrations.AlterUniqueTogether(
            name='dresssize',
            unique_together=set([('name', 'sort_key')]),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('ophase', 'email')]),
        ),
    ]
