# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-06 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20160905_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='oracle_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Oracle Code'),
        ),
    ]