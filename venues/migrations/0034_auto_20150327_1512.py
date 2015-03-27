# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0033_remove_report_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmasjid',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='created_by_ip',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
