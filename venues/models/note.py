from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

__author__ = 'm'


class Note(models.Model):
    '''
    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    # modified info
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created_by",
                                   default=None, null=True, blank=True)

    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="%(class)s_modified_by",
                                   default=None, null=True, blank=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)

    # venue info
    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')

    text = models.TextField(max_length=200, blank=True)

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
