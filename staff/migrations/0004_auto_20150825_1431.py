# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20150712_2044'),
        ('ophasebase', '0003_auto_20150825_1433'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Gruppenkategorien',
                'verbose_name': 'Gruppenkategorie',
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations),
        migrations.AlterField(
            model_name='person',
            name='tutor_for',
            field=models.ForeignKey(to='staff.GroupCategory', help_text='Erstsemester welches Studiengangs möchtest du als Tutor betreuen?', null=True, blank=True, verbose_name='Tutor für'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='group_categories_enabled',
            field=models.ManyToManyField(to='staff.GroupCategory', verbose_name='Freigeschaltete Kleingruppenkategorien'),
        ),
    ]
