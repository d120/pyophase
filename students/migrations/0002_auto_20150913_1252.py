# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorgroup',
            name='tutors',
            field=models.ManyToManyField(blank=True, verbose_name='Tutoren', to='staff.Person'),
        ),
    ]
