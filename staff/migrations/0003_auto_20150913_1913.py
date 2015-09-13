# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_tutorgroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tutorgroup',
            unique_together=set([('ophase', 'name')]),
        ),
    ]
