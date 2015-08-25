# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20150825_1552'),
        ('ophasebase', '0005_auto_20150825_1552'),
    ]

    state_operations = [
        migrations.DeleteModel(
            name='HelperJob',
        ),
        migrations.DeleteModel(
            name='OrgaJob',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
