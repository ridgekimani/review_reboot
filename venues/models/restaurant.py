from django.core.urlresolvers import reverse
from django.db import models
from simple_history.models import HistoricalRecords
from venues.models import Venue
from venues.models.cuisine import Cuisine

from django.core.validators import MaxLengthValidator

__author__ = 'm'

# simple_history will add its tables to db only if field added to model class,
# not a parent class (Venue)
class Restaurant(Venue):
    MENU_TYPES = (
        (0, "?"),
        (1, "Partially Halal"),
        (2, "Full Halal"),
    )

    CHOICES = (
        (None, "?"),
        (False, "No"),
        (True, "Yes"),
    )

    history_link = HistoricalRecords()

    menu = models.IntegerField(default=0, choices=MENU_TYPES)
    about = models.TextField(blank=True)

    shop_number = models.CharField(max_length=50, blank=True)

    website = models.URLField(default="", blank=True)

    google_reviews_url = models.URLField(default="", blank=True)
    yelp_url = models.URLField(default="", blank=True)
    foursquare_url = models.URLField(default="", blank=True)


    catering = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    delivery = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    alcoholFree = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    porkFree = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    muslimOwner = models.NullBooleanField(null=True, blank=True, choices=CHOICES)

    cuisines = models.ManyToManyField(Cuisine, null=True, default=None)


    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value

    def show_url(self):
        return reverse("venues.views.venuess.restaurant", args=[self.id])

    def edit_url(self):
        return reverse("venues.views.venuess.update_restaurant", args=[self.id])

    def remove_url(self):
        return reverse("venues.views.venuess.suspend_restaurant", args=[self.id])

    def add_url(self):
        return reverse("venues.views.venuess.add_restaurant")