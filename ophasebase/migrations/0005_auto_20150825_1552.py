# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0004_auto_20150825_1509'),
    ]

    database_operations = [
        migrations.AlterModelTable('orgajob', 'staff_orgajob'),
        migrations.AlterModelTable('helperjob', 'staff_helperjob'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(database_operations=database_operations)
    ]
