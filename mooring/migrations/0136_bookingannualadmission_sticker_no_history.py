# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-07-23 05:41
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0135_bookingannualinvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingannualadmission',
            name='sticker_no_history',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[], null=True),
        ),
    ]
