# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0015_auto_20150312_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='modified_ip',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='modified_on',
        ),
        migrations.RemoveField(
            model_name='report',
            name='opened_by',
        ),
        migrations.AddField(
            model_name='note',
            name='modified_by',
            field=models.ForeignKey(related_name='note_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='created_by',
            field=models.ForeignKey(related_name='report_created_by', default=None, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
