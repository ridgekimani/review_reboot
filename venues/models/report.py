from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
import venues.models.restaurant
import venues.models.venue
from venues.models.restaurant import Restaurant

class ReportType(models.Model):
    report_type = models.CharField(max_length=200)

    CHOICES = (
        ('restaurant','Restaurnat'),
        ('masjid', 'Masjid')
    )

    venue_type = models.CharField(max_length=20, default='restaurant', choices=CHOICES)

    def __unicode__(self):
        return self.report_type

class Report(models.Model):
    '''
    Represents table row with user report for venue
    '''
    class Meta:
        ordering = ['resolved', '-created_on']

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

    report_type = models.ManyToManyField(ReportType)
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
            self.venue_name, '\n'
            'report:', [ n.report_type.__str__() for n in self.report_type.get_queryset() ].__str__(), '\n'
            'note:', self.note
        ])

    @property
    def venue_name(self):
        if self.content_object:
            return self.content_object.name
        else:
            return ""
