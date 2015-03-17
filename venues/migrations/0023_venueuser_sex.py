# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0022_auto_20150317_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='venueuser',
            name='sex',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'male'), (1, b'female'), (2, b'not defined')]),
            preserve_default=True,
        ),
    ]
