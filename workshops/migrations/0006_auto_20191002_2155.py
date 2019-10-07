# Generated by Django 2.2.6 on 2019-10-02 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ophasebase', '0008_auto_20190226_1853'),
        ('workshops', '0005_auto_20160820_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='possible_slots',
            field=models.ManyToManyField(help_text='Welche Slots sind zeitlich möglich (unabhängig davon wie oft der Workshop stattfinden kann)?', related_name='possible_workshops', to='workshops.WorkshopSlot', verbose_name='Mögliche Zeitslots'),
        ),
        migrations.CreateModel(
            name='WorkshopAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_location', models.CharField(blank=True, help_text='Freitext-Feld für zugewiesenen Raum', max_length=200, null=True, verbose_name='Zugewiesener Ort')),
                ('assigned_room', models.ForeignKey(blank=True, help_text='In welchem Raum findet der Workshop statt?', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ophasebase.Room', verbose_name='Zugewiesener Raum')),
                ('assigned_slot', models.ForeignKey(help_text='Wann findet der Workshop statt?', on_delete=django.db.models.deletion.CASCADE, to='workshops.WorkshopSlot', verbose_name='Zugewiesener Zeitslot')),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshops.Workshop')),
            ],
            options={
                'verbose_name': 'Workshopzuordnung',
                'verbose_name_plural': 'Workshopzuordnungen',
            },
        ),
        migrations.AddField(
            model_name='workshop',
            name='assigned',
            field=models.ManyToManyField(help_text='Wann und Wo findet der Workshop statt?', related_name='assigned_workshops', through='workshops.WorkshopAssignment', to='workshops.WorkshopSlot', verbose_name='Zugewiesene Zeitslots und Orte'),
        ),
    ]