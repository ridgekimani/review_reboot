# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'venues_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'venues', ['Category'])

        # Adding model 'HistoricalRestaurant'
        db.create_table(u'venues_historicalrestaurant', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('avg_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('closed_reports_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('cuisine', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('eatingOptions', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('yelp_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('yelp_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('foursquare_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('foursquare_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')()),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'venues', ['HistoricalRestaurant'])

        # Adding model 'Restaurant'
        db.create_table(u'venues_restaurant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('avg_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('closed_reports_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('cuisine', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('eatingOptions', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('yelp_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('yelp_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('foursquare_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('foursquare_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'venues', ['Restaurant'])

        # Adding M2M table for field categories on 'Restaurant'
        m2m_table_name = db.shorten_name(u'venues_restaurant_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm[u'venues.restaurant'], null=False)),
            ('category', models.ForeignKey(orm[u'venues.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['restaurant_id', 'category_id'])

        # Adding model 'HistoricalMasjid'
        db.create_table(u'venues_historicalmasjid', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('avg_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('closed_reports_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('twitter_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')()),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'venues', ['HistoricalMasjid'])

        # Adding model 'Masjid'
        db.create_table(u'venues_masjid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('avg_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('closed_reports_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('twitter_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'venues', ['Masjid'])

        # Adding M2M table for field categories on 'Masjid'
        m2m_table_name = db.shorten_name(u'venues_masjid_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('masjid', models.ForeignKey(orm[u'venues.masjid'], null=False)),
            ('category', models.ForeignKey(orm[u'venues.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['masjid_id', 'category_id'])

        # Adding model 'Comment'
        db.create_table(u'venues_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('venue_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'venues', ['Comment'])

        # Adding model 'Tip'
        db.create_table(u'venues_tip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('venue_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'venues', ['Tip'])

        # Adding model 'Report'
        db.create_table(u'venues_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='report_user', null=True, to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('venue_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('report', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='report_moderator', null=True, to=orm['auth.User'])),
            ('moderator_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('moderator_note', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'venues', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'venues_category')

        # Deleting model 'HistoricalRestaurant'
        db.delete_table(u'venues_historicalrestaurant')

        # Deleting model 'Restaurant'
        db.delete_table(u'venues_restaurant')

        # Removing M2M table for field categories on 'Restaurant'
        db.delete_table(db.shorten_name(u'venues_restaurant_categories'))

        # Deleting model 'HistoricalMasjid'
        db.delete_table(u'venues_historicalmasjid')

        # Deleting model 'Masjid'
        db.delete_table(u'venues_masjid')

        # Removing M2M table for field categories on 'Masjid'
        db.delete_table(db.shorten_name(u'venues_masjid_categories'))

        # Deleting model 'Comment'
        db.delete_table(u'venues_comment')

        # Deleting model 'Tip'
        db.delete_table(u'venues_tip')

        # Deleting model 'Report'
        db.delete_table(u'venues_report')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'venues.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'venues.comment': {
            'Meta': {'object_name': 'Comment'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'venues.historicalmasjid': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalMasjid'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'avg_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'closed_reports_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'modified_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'twitter_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'venues.historicalrestaurant': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalRestaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'avg_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'closed_reports_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cuisine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'eatingOptions': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'foursquare_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'modified_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'yelp_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'yelp_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'venues.masjid': {
            'Meta': {'object_name': 'Masjid'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'avg_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['venues.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'closed_reports_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'twitter_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'venues.report': {
            'Meta': {'object_name': 'Report'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'report_moderator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'moderator_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderator_note': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'report_user'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'venues.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'avg_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['venues.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'closed_reports_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cuisine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'eatingOptions': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'foursquare_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'yelp_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'yelp_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'venues.tip': {
            'Meta': {'object_name': 'Tip'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['venues']