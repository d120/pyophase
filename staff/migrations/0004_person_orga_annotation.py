# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20150913_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='orga_annotation',
            field=models.TextField(help_text='Notizen von Leitung und Orgas.', verbose_name='Orga-Anmerkungen', blank=True),
        ),
    ]
