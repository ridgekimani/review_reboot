# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0005_auto_20150309_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='masjid',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='menu',
            field=models.IntegerField(default=0, choices=[(0, b'-'), (1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='menu',
            field=models.IntegerField(default=0, choices=[(0, b'-'), (1, b'Partially Halal'), (2, b'Full Halal')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'Yes'), (True, b'No')]),
            preserve_default=True,
        ),
    ]
