# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0008_auto_20150312_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report',
            field=models.CharField(max_length=30, choices=[(1, b'Closed'), (2, b'Is a duplicate'), (3, b'Wrong Location'), (4, b'Other')]),
            preserve_default=True,
        ),
    ]
