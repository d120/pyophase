# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150913_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorgroup',
            name='group_category',
        ),
        migrations.RemoveField(
            model_name='tutorgroup',
            name='ophase',
        ),
        migrations.RemoveField(
            model_name='tutorgroup',
            name='tutors',
        ),
        migrations.AlterField(
            model_name='student',
            name='tutor_group',
            field=models.ForeignKey(verbose_name='Kleingruppe', to='staff.TutorGroup', on_delete=models.CASCADE),
        ),
        migrations.DeleteModel(
            name='TutorGroup',
        ),
    ]
