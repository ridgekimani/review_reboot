# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_auto_20150309_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrestaurant',
            name='google_reviews_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='link',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='google_reviews_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='link',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
    ]
