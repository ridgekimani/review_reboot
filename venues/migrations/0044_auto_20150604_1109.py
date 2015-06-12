# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0043_auto_20150604_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttype',
            name='venue_type',
            field=models.CharField(default=b'restaurant', max_length=20, choices=[(b'restaurant', b'Restaurnat'), (b'masjid', b'Masjid')]),
            preserve_default=True,
        ),
    ]
