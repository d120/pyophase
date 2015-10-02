# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20150913_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Newsletter')),
                ('description', models.TextField(verbose_name='Beschreibung')),
                ('active', models.BooleanField(default=True, verbose_name='Auswählbar')),
            ],
            options={
                'verbose_name': 'Newsletter',
                'ordering': ['active', 'name'],
                'verbose_name_plural': 'Newsletter',
            },
        ),
    ]
