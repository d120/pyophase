# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0002_auto_20150626_2024'),
    ]

    database_operations = [
        migrations.AlterModelTable('groupcategory', 'staff_groupcategory'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(database_operations=database_operations)
    ]
