# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('venue_id', models.PositiveIntegerField(editable=False)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('text', models.TextField(blank=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalMasjid',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^[0-9 -]+$', message=b'Only digits allowed')])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='Latitude/Longitude', blank=True)),
                ('avg_rating', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('closed_reports_count', models.IntegerField(default=0)),
                ('is_closed', models.BooleanField(default=False)),
                ('modified_by_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('modified_on', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('twitter_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('facebook_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical masjid',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalRestaurant',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^[0-9 -]+$', message=b'Only digits allowed')])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='Latitude/Longitude', blank=True)),
                ('avg_rating', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('closed_reports_count', models.IntegerField(default=0)),
                ('is_closed', models.BooleanField(default=False)),
                ('modified_by_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('modified_on', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('cuisine', models.CharField(max_length=50)),
                ('eatingOptions', models.CharField(max_length=50)),
                ('yelp_id', models.CharField(max_length=255, blank=True)),
                ('yelp_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('foursquare_id', models.CharField(max_length=100, blank=True)),
                ('foursquare_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical restaurant',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Masjid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^[0-9 -]+$', message=b'Only digits allowed')])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='Latitude/Longitude', blank=True)),
                ('avg_rating', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('closed_reports_count', models.IntegerField(default=0)),
                ('is_closed', models.BooleanField(default=False)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('twitter_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('facebook_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('categories', models.ManyToManyField(to='venues.Category', null=True)),
                ('modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('venue_id', models.PositiveIntegerField(editable=False)),
                ('text', models.TextField(max_length=200, blank=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('venue_id', models.PositiveIntegerField(editable=False)),
                ('report', models.CharField(max_length=30, choices=[(b'closed', b'Closed'), (b'is_duplicate', b'Is a duplicate'), (b'wrong_location', b'Wrong Location'), (b'other', b'Other')])),
                ('note', models.TextField(blank=True)),
                ('moderator_flag', models.BooleanField(default=False)),
                ('moderator_note', models.TextField(null=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType')),
                ('moderator', models.ForeignKey(related_name='report_moderator', default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='report_user', default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(regex=b'^[0-9 -]+$', message=b'Only digits allowed')])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True, verbose_name='Latitude/Longitude', blank=True)),
                ('avg_rating', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('closed_reports_count', models.IntegerField(default=0)),
                ('is_closed', models.BooleanField(default=False)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('modified_ip', models.CharField(default=b'', max_length=39, editable=False)),
                ('cuisine', models.CharField(max_length=50)),
                ('eatingOptions', models.CharField(max_length=50)),
                ('yelp_id', models.CharField(max_length=255, blank=True)),
                ('yelp_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('foursquare_id', models.CharField(max_length=100, blank=True)),
                ('foursquare_url', models.CharField(blank=True, max_length=255, validators=[django.core.validators.URLValidator()])),
                ('categories', models.ManyToManyField(to='venues.Category', null=True)),
                ('modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
