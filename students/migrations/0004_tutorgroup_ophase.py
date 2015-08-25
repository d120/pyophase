# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from ophasebase.models import Ophase


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0007_auto_20150825_1722'),
        ('students', '0003_auto_20150825_1722'),
    ]

    try:
        active_ophase_id = Ophase.objects.filter(is_active=True)[0].id
    except:
        active_ophase_id = 0

    operations = [
        migrations.AddField(
            model_name='tutorgroup',
            name='ophase',
            field=models.ForeignKey(default=active_ophase_id, to='ophasebase.Ophase'),
            preserve_default=False,
        ),
    ]
