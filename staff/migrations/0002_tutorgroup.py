# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Gruppenname', max_length=50)),
                ('group_category', models.ForeignKey(verbose_name='Gruppenkategorie', to='staff.GroupCategory', on_delete=models.CASCADE)),
                ('ophase', models.ForeignKey(to='ophasebase.Ophase', on_delete=models.CASCADE)),
                ('tutors', models.ManyToManyField(verbose_name='Tutoren', blank=True, to='staff.Person')),
            ],
            options={
                'verbose_name_plural': 'Kleingruppen',
                'verbose_name': 'Kleingruppe',
                'ordering': ['group_category', 'name'],
            },
        ),
    ]
