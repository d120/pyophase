# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('ophasebase', '0003_auto_20150825_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorgroup',
            name='groupCategory',
            field=models.ForeignKey(to='staff.GroupCategory', verbose_name='Gruppenkategorie'),
        ),
    ]
