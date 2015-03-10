# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0006_auto_20150310_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='link',
            new_name='website',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='link',
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='foursquare_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='website',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='yelp_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='foursquare_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='yelp_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
    ]
