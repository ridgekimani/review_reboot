from django.db import models
from simple_history.models import HistoricalRecords
from venues.models import Venue

__author__ = 'm'

# simple_history will add its tables to db only if field added to model class,
# not a parent class (Venue)
class Restaurant(Venue):
    MENU_TYPES = (
        (0, "-"),
        (1, "Partially Halal"),
        (2, "Full Halal"),
    )

    CHOICES = (
        (None, "-"),
        (False, "Yes"),
        (True, "No"),
    )

    history_link = HistoricalRecords()

    cuisine = models.CharField(max_length=50)
    menu = models.IntegerField(default=0, choices=MENU_TYPES)

    link = models.URLField(default="")
    google_reviews_url = models.URLField(default="")

    catering = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    delivery = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    alcoholFree = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    porkFree = models.NullBooleanField(null=True, blank=True, choices=CHOICES)
    muslimOwner = models.NullBooleanField(null=True, blank=True, choices=CHOICES)

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value
