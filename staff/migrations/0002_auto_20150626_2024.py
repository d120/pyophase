# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0002_auto_20150626_2024'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='group_categories_enabled',
            field=models.ManyToManyField(verbose_name='Freigeschaltete Kleingruppenkategorien', to='ophasebase.GroupCategory'),
        ),
        migrations.AddField(
            model_name='settings',
            name='helper_jobs_enabled',
            field=models.ManyToManyField(verbose_name='Freigeschaltete Helferjobs', to='ophasebase.HelperJob'),
        ),
        migrations.AddField(
            model_name='settings',
            name='orga_jobs_enabled',
            field=models.ManyToManyField(verbose_name='Freigeschaltete Orgajobs', to='ophasebase.OrgaJob'),
        ),
    ]
