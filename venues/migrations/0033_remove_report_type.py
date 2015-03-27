# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0032_auto_20150326_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='type',
        ),
    ]
