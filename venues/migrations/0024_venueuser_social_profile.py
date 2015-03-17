# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0023_venueuser_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='venueuser',
            name='social_profile',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
