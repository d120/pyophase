# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'verbose_name_plural': 'Klausurzuteilungen', 'verbose_name': 'Klausurzuteilung', 'get_latest_by': 'created_at', 'ordering': ['-created_at']},
        ),
    ]
