# Generated by Django 2.0.9 on 2018-10-08 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0008_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Kommentar'),
        ),
    ]