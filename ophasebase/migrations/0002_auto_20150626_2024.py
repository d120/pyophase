# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helperjob',
            name='has_enough_persons',
        ),
        migrations.RemoveField(
            model_name='ophase',
            name='group_categories',
        ),
        migrations.RemoveField(
            model_name='ophase',
            name='helper_jobs',
        ),
        migrations.RemoveField(
            model_name='ophase',
            name='orga_jobs',
        ),
        migrations.RemoveField(
            model_name='orgajob',
            name='has_enough_persons',
        ),
    ]
