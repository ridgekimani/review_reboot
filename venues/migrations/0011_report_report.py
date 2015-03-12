# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0010_remove_report_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report',
            field=models.IntegerField(default=4, choices=[(1, b'Closed'), (2, b'Is a duplicate'), (3, b'Wrong Location'), (4, b'Other')]),
            preserve_default=True,
        ),
    ]
