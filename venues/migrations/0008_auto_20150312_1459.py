# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0007_auto_20150310_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmasjid',
            name='city',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalmasjid',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='city',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masjid',
            name='city',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masjid',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2),
            preserve_default=False,
        ),
    ]
