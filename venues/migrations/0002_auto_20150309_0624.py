# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='eatingOptions',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='foursquare_id',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='foursquare_url',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='yelp_id',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='yelp_url',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='eatingOptions',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='foursquare_id',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='foursquare_url',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='yelp_id',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='yelp_url',
        ),
        migrations.AddField(
            model_name='historicalmasjid',
            name='approved',
            field=models.BooleanField(default=False, help_text='Is this venue approved by moderator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='alcoholFree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='approved',
            field=models.BooleanField(default=False, help_text='Is this venue approved by moderator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='catering',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='delivery',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='menu',
            field=models.IntegerField(default=1, choices=[(1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='muslimOwner',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='porkFree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='approved',
            field=models.BooleanField(default=False, help_text='Is this venue approved by moderator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='alcoholFree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='approved',
            field=models.BooleanField(default=False, help_text='Is this venue approved by moderator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='catering',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='delivery',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='menu',
            field=models.IntegerField(default=1, choices=[(1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='muslimOwner',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='porkFree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
