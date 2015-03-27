from django.contrib.auth.models import User

from django.core.validators import RegexValidator, URLValidator
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords
from venues.models._common import CommonModel


__author__ = 'm'

# Create your models here.
class Venue(CommonModel):
    '''
    General model for venues.
    '''

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

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

    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    is_closed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, help_text=u"Is this venue approved by moderator")
    review_count = models.IntegerField(default=0)

    is_suspended = models.BooleanField(default=False)
    # Query Manager
    gis = gis_models.GeoManager()
    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def update_avg_rating(self):
        from venues.models import Review
        self_reviews = Review.objects.filter(venue_id=self.id)
        num_of_reviews = float(len(self_reviews))
        if num_of_reviews == 0.0:
            return
        avg_rating = 0.0
        for review in self_reviews:
            avg_rating += review.rating / num_of_reviews
        self.avg_rating = avg_rating
        self.save()

    def update_review_counter(self):
        from venues.models import Review
        self_reviews_count = Review.objects.filter(venue_id=self.id).count()
        if self_reviews_count == 0:
            return
        self.review_count = self_reviews_count
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






