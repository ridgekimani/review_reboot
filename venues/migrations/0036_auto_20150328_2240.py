# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0035_auto_20150327_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venueuser',
            name='venue_moderator',
            field=models.BooleanField(default=False, help_text=b'User can approve, remove, and see suspended venues'),
            preserve_default=True,
        ),
    ]
