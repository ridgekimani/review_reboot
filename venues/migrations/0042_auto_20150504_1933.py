# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0041_auto_20150330_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='historicalmasjid',
            name='sect_id',
            field=models.IntegerField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='masjid',
            name='sect',
            field=models.ForeignKey(default=None, to='venues.Sect', null=True),
            preserve_default=True,
        ),
    ]
