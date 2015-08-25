# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0006_auto_20150825_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='hasBeamer',
            new_name='has_beamer',
        ),
    ]
