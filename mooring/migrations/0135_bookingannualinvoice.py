# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-07-10 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0134_auto_20200710_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingAnnualInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_reference', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('system_invoice', models.BooleanField(default=False)),
                ('booking_annual_admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annual_booking_invoices', to='mooring.BookingAnnualAdmission')),
            ],
        ),
    ]
