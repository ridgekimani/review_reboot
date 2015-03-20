from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
import venues.models.restaurant
import venues.models.venue
from venues.models.restaurant import Restaurant

class Report(models.Model):
    '''
    Represents table row with user report for venue
    '''
    class Meta:
        ordering = ['resolved', '-created_on']

    REPORTS = (
        (1, 'No longer Halal :('),
        (2, 'Address is Da`eef'),
        (3, 'Incorrect address'),
        (4, 'Incorrect Map Pin'),
        (5, 'Out of business'),
        (6, 'Other')
    )

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        null=True,
        default=None,
        related_name="%(class)s_created_by",
        editable=False
    )
    closed_by = models.ForeignKey(
        User,
        null=True,
        default=None,
        related_name="%(class)s_closed_by",
        editable=False
    )
    resolved = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')

    type = models.IntegerField(choices=REPORTS, default=4)
    note = models.TextField(blank=True)

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
                                                           'report:', self.get_type_display(), '\n'
                                                                                                 'note:', self.note
        ])

    @property
    def venue_name(self):
        return self.content_object.name
