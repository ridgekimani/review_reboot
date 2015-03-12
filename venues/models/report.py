from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
import venues.models.restaurant
import venues.models.venue


class Report(models.Model):
    '''
    Represents table row with user report for venue

    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    REPORTS = (
        (1, 'Closed'),
        (2, 'Is a duplicate'),
        (3, 'Wrong Location'),
        (4, 'Other')
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        null=True,
        default=None,
        related_name='report_user'
    )
    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')
    type = models.IntegerField(choices=REPORTS, default=4)
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
            venues.Restaurant.objects.get(id=self.venue_id).name, '\n'
                                                           'report:', self.get_type_display(), '\n'
                                                                                                 'note:', self.note
        ])

    @property
    def venue_name(self):
        return self.content_object.name
