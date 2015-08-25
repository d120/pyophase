# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150825_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Erstie', 'ordering': ['tutor_group', 'name', 'prename'], 'verbose_name_plural': 'Ersties'},
        ),
        migrations.AlterModelOptions(
            name='tutorgroup',
            options={'verbose_name': 'Kleingruppe', 'ordering': ['group_category', 'name'], 'verbose_name_plural': 'Kleingruppen'},
        ),
        migrations.RenameField(
            model_name='student',
            old_name='tutorGroup',
            new_name='tutor_group',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='wantExam',
            new_name='want_exam',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='wantNewsletter',
            new_name='want_newsletter',
        ),
        migrations.RenameField(
            model_name='tutorgroup',
            old_name='groupCategory',
            new_name='group_category',
        ),
    ]
