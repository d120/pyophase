# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_newsletter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'verbose_name_plural': 'Newsletter', 'ordering': ['-active', 'name'], 'verbose_name': 'Newsletter'},
        ),
        migrations.AddField(
            model_name='student',
            name='newsletters',
            field=models.ManyToManyField(to='students.Newsletter', help_text='Welche Newsletter willst du abonieren (optional)?', verbose_name='Newsletter', blank=True),
        ),
    ]
