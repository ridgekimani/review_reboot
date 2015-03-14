# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('venues', '0020_comment_approved'),
    ]

    operations = [
        migrations.RenameModel(
            'Comment',
            'Review'
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['resolved', '-created_on']},
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalrestaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='alcoholFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='catering',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='cuisines',
            field=models.ManyToManyField(default=None, to='venues.Cuisine', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='delivery',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='muslimOwner',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='porkFree',
            field=models.NullBooleanField(choices=[(None, b'-'), (False, b'No'), (True, b'Yes')]),
            preserve_default=True,
        ),
    ]
