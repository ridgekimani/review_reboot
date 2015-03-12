# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0009_auto_20150312_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='report',
        ),
    ]
