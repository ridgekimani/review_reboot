# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0036_auto_20150328_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmasjid',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
            preserve_default=True,
        ),
    ]
