# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20150929_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='want_newsletter',
        ),
    ]
