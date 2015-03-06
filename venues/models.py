from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, URLValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from simple_history.models import HistoricalRecords

import datetime


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Create your models here.
class Venue(models.Model):
    '''
    General model for venues.
    '''
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    address = models.CharField(max_length=150)
    phone = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9 -]+$',
                message='Only digits allowed'
            )
        ]
    )
    location = gis_models.PointField(
        u'Latitude/Longitude',
        geography=True,
        blank=True,
        null=True
    )
    categories = models.ManyToManyField(Category, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    closed_reports_count = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)

    # Potentially User can make changes in this model
    modified_by = models.ForeignKey(User, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)


    # Query Manager
    gis = gis_models.GeoManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def update_avg_rating(self):
        self_comments = Comment.objects.filter(venue_id=self.id)
        num_of_comments = float(len(self_comments))
        if num_of_comments == 0.0:
            return
        avg_rating = 0.0
        for comment in self_comments:
            avg_rating += comment.rating / num_of_comments
        self.avg_rating = avg_rating
        self.save()

    def update_close_state(self):
        close_reports = Report.objects.filter(
            venue_id=self.id,
            report='closed'
        )
        self.closed_reports_count = len(close_reports)
        if len(close_reports) > 3:
            self.is_closed = True
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Venue, self).save(args, kwargs)


# simple_history will add its tables to db only if field added to model class,
# not a parent class (Venue)
class Restaurant(Venue):
    cuisine = models.CharField(max_length=50)
    eatingOptions = models.CharField(max_length=50)
    yelp_id = models.CharField(max_length=255, blank=True)
    yelp_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])
    foursquare_id = models.CharField(max_length=100, blank=True)
    foursquare_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])

    # django-simple-history code
    history_link = HistoricalRecords()

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value


# simple_history will add its tables to db only if field added to model class,
# not a parent class (Venue)
class Masjid(Venue):
    url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])
    twitter_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])
    facebook_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])

    # django-simple-history code
    history_link = HistoricalRecords()

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value


class Comment(models.Model):
    '''
    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')
    rating = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)

    @staticmethod
    def list_for_venue(venue):
        related_object_type = ContentType.objects.get_for_model(venue)
        return Comment.objects.filter(content_type__pk=related_object_type.id,
                                      venue_id=venue.id)

    @property
    def venue_name(self):
        return self.content_object.name

    def __unicode__(self):
        return self.text[:25]

    @property
    def short_text(self):
        return self.__unicode__()


class Note(models.Model):
    '''
    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType,editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')
    text = models.TextField(max_length=200, blank=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)

    @staticmethod
    def list_for_venue(venue):
        related_object_type = ContentType.objects.get_for_model(venue)
        return Note.objects.filter(content_type__pk=related_object_type.id,
                                      venue_id=venue.id)

    def __unicode__(self):
        return self.text[:25]

    @property
    def venue_name(self):
        return self.content_object.name


class Report(models.Model):
    '''
    Represents table row with user report for venue

    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    REPORTS = (
        ('closed', 'Closed'),
        ('is_duplicate', 'Is a duplicate'),
        ('wrong_location', 'Wrong Location'),
        ('other', 'Other')
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        null=True,
        default=None,
        related_name='report_user'
    )
    content_type = models.ForeignKey(ContentType,editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')
    report = models.CharField(choices=REPORTS, max_length=30)
    note = models.TextField(blank=True)
    moderator = models.ForeignKey(
        User,
        null=True,
        default=None,
        related_name='report_moderator'
    )
    moderator_flag = models.BooleanField(default=False)
    moderator_note = models.TextField(null=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)

    @staticmethod
    def list_for_venue(venue):
        related_object_type = ContentType.objects.get_for_model(venue)
        return Report.objects.filter(content_type__pk=related_object_type.id,
                                      venue_id=venue.id)


    def __unicode__(self):
        return u' '.join([
            Restaurant.objects.get(id=self.venue_id).name, '\n'
                                                           'report:', self.get_report_display(), '\n'
                                                                                                 'note:', self.note
        ])

    @property
    def venue_name(self):
        return self.content_object.name