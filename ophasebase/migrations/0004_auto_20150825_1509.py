# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0003_auto_20150825_1433'),
        ('staff', '0004_auto_20150825_1431'),
        ('students', '0002_auto_20150825_1431')
    ]

    state_operations = [
        migrations.DeleteModel(
            name='GroupCategory',
        )
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
