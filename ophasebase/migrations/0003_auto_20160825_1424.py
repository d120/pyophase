# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0002_ophase_contact_email_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ophase',
            name='contact_email_address',
            field=models.EmailField(max_length=254, verbose_name='Kontaktadresse Leitung'),
        ),
    ]
