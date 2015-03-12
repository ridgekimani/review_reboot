# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0016_auto_20150312_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(related_name='comment_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 32, 405423, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_by',
            field=models.ForeignKey(related_name='comment_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_ip',
            field=models.CharField(default=b'', max_length=39, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 35, 836414, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalmasjid',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 37, 833889, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalrestaurant',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 40, 518777, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masjid',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 42, 558638, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 44, 372583, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalmasjid',
            name='created_by_id',
            field=models.IntegerField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalmasjid',
            name='modified_by_id',
            field=models.IntegerField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalmasjid',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 46, 178922, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='created_by_id',
            field=models.IntegerField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='modified_by_id',
            field=models.IntegerField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 50, 358222, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='created_by',
            field=models.ForeignKey(related_name='masjid_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='modified_by',
            field=models.ForeignKey(related_name='masjid_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='masjid',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 52, 357404, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='created_by',
            field=models.ForeignKey(related_name='restaurant_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='modified_by',
            field=models.ForeignKey(related_name='restaurant_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='modified_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 17, 44, 54, 211852, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
