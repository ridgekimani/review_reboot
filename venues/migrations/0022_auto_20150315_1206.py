# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0021_auto_20150314_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.IntegerField(default=4, choices=[(1, b'No longer Halal :('), (2, b'Address is Da`eef'), (3, b'Incorrect address'), (4, b'Incorrect Map Pin'), (5, b'Out of business'), (6, b'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='created_by',
            field=models.ForeignKey(related_name='review_created_by', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='modified_by',
            field=models.ForeignKey(related_name='review_modified_by', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
