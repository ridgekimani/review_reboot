# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0042_auto_20150504_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporttype',
            name='venue_type',
            field=models.CharField(default=b'restaurant', max_length=20, choices=[(b'restaurnat', b'Restaurnat'), (b'masjid', b'Masjid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='foursquare_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='google_reviews_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='yelp_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='foursquare_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='google_reviews_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='yelp_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
