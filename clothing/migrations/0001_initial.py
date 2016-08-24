# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0007_auto_20160711_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, unique=True, verbose_name='Farbe')),
                ('color_code', models.CharField(default='#FFFFFF', max_length=7, verbose_name='Farbcode')),
            ],
            options={
                'verbose_name_plural': 'Farben',
                'verbose_name': 'Farbe',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional', models.BooleanField(verbose_name='Zusätzliches Kleidungsstück')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothing.Color')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Person')),
            ],
            options={
                'verbose_name_plural': 'Bestellungen',
                'verbose_name': 'Bestellung',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=75, unique=True, verbose_name='Größe')),
            ],
            options={
                'verbose_name_plural': 'Größen',
                'verbose_name': 'Größe',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, unique=True, verbose_name='Art')),
                ('price', models.FloatField(verbose_name='Preis')),
            ],
            options={
                'ordering': ['-price', 'name'],
                'verbose_name_plural': 'Arten',
                'verbose_name': 'Art',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothing.Size'),
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothing.Type'),
        ),
    ]