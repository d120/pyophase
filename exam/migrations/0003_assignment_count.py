# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_assignment_persontoexamroomassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='count',
            field=models.PositiveIntegerField(verbose_name='# Zuteilungen', default=0),
            preserve_default=False,
        ),
    ]
