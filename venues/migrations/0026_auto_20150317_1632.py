# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0025_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venueuser',
            name='sex',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'Male'), (1, b'Female')]),
            preserve_default=True,
        ),
    ]
