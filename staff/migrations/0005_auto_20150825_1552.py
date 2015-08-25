# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20150825_1431'),
        ('ophasebase', '0005_auto_20150825_1552'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='HelperJob',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Helferjobs',
                'verbose_name': 'Helferjob',
            },
        ),
        migrations.CreateModel(
            name='OrgaJob',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Orgajobs',
                'verbose_name': 'Orgajob',
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations),
        migrations.AlterField(
            model_name='person',
            name='helper_jobs',
            field=models.ManyToManyField(blank=True, help_text='Bei welchen Aufgaben kannst du dir vorstellen zu helfen?', verbose_name='Helferaufgaben', to='staff.HelperJob'),
        ),
        migrations.AlterField(
            model_name='person',
            name='orga_jobs',
            field=models.ManyToManyField(blank=True, help_text='Welche Orgaaufgaben kannst du dir vorstellen zu übernehmen?', verbose_name='Orgaaufgaben', to='staff.OrgaJob'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='helper_jobs_enabled',
            field=models.ManyToManyField(verbose_name='Freigeschaltete Helferjobs', to='staff.HelperJob'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='orga_jobs_enabled',
            field=models.ManyToManyField(verbose_name='Freigeschaltete Orgajobs', to='staff.OrgaJob'),
        ),
    ]
