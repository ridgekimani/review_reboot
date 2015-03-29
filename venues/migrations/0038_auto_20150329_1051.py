# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0037_auto_20150329_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrestaurant',
            name='about',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='about',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
