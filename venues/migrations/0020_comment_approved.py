# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0019_auto_20150312_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
