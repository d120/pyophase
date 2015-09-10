# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_assignment_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='selected_rooms',
        ),
    ]
