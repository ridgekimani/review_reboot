# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0034_auto_20150327_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmasjid',
            name='is_suspended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='is_suspended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='is_suspended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='is_suspended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
