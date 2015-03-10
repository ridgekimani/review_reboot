# simple_history will add its tables to db only if field added to model class,
# not a parent class (Venue)
from django.core.validators import URLValidator
from django.db import models
from simple_history.models import HistoricalRecords
from venues.models import Venue


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
