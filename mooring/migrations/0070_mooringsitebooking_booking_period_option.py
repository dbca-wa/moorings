# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-08 07:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0069_auto_20181106_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='mooringsitebooking',
            name='booking_period_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='booking_period_option', to='mooring.BookingPeriodOption'),
        ),
    ]
