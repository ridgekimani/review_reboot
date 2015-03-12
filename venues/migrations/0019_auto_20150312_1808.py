# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0018_auto_20150312_1754'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Cuisine',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='categories',
            new_name='cuisines',
        ),
        migrations.RemoveField(
            model_name='historicalrestaurant',
            name='cuisine',
        ),
        migrations.RemoveField(
            model_name='masjid',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='cuisine',
        ),
    ]
