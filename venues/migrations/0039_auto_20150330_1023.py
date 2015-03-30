# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0038_auto_20150329_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrestaurant',
            name='address_note',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(200)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='address_note',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(200)]),
            preserve_default=True,
        ),
    ]
