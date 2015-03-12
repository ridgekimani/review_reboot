from django.contrib.auth.models import User

from django.core.validators import RegexValidator, URLValidator
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords
from venues.models.category import Category


__author__ = 'm'

# Create your models here.
class Venue(models.Model):
    '''
    General model for venues.
    '''

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country = CountryField()

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
    approved = models.BooleanField(default=False, help_text=u"Is this venue approved by moderator")


    # Potentially User can make changes in this model
    modified_by = models.ForeignKey(User, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)
    modified_ip = models.CharField(default='', max_length=39, editable=False)


    # Query Manager
    gis = gis_models.GeoManager()
    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def update_avg_rating(self):
        from venues.models.comment import Comment
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
        from venues.models.report import Report
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

    @property
    def show_url(self):
        """
        :return: show url of item
        """
        return ""

    @property
    def add_url(self):
        """
        :return: add url of item
        """
        return ""

    @property
    def edit_url(self):
        """
        :return: edit url of item
        """
        return ""

    @property
    def remove_url(self):
        """
        :return: remove url of item
        """
        return ""






