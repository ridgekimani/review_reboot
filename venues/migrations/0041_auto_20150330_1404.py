# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0040_auto_20150330_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrestaurant',
            name='shop_number',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='shop_number',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
