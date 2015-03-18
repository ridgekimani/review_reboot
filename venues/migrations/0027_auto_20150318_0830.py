# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0026_auto_20150317_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'?'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
    ]
