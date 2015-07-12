# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_auto_20150626_2024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('ophase', 'email')]),
        ),
    ]
