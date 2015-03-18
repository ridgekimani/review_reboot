# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0027_auto_20150318_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='menu',
            field=models.IntegerField(default=0, choices=[(0, b'?'), (1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='menu',
            field=models.IntegerField(default=0, choices=[(0, b'?'), (1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
    ]
