# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0028_auto_20150318_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='website',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='website',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
