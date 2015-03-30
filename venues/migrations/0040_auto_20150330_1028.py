# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0039_auto_20150330_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmasjid',
            name='address_note',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(200)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='address_note',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(200)]),
            preserve_default=True,
        ),
    ]
