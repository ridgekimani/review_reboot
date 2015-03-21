# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0030_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmasjid',
            name='review_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='review_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='review_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='review_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
