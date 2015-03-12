# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0013_auto_20150312_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmasjid',
            name='created_by_id',
            field=models.IntegerField(db_index=True, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalmasjid',
            name='modified_by_id',
            field=models.IntegerField(db_index=True, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='created_by_id',
            field=models.IntegerField(db_index=True, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='modified_by_id',
            field=models.IntegerField(db_index=True, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='created_by',
            field=models.ForeignKey(related_name='masjid_created_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='modified_by',
            field=models.ForeignKey(related_name='masjid_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='created_by',
            field=models.ForeignKey(related_name='restaurant_created_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='modified_by',
            field=models.ForeignKey(related_name='restaurant_modified_by', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
