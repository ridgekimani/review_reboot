# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0011_report_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='report',
            new_name='type',
        ),
    ]
