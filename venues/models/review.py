from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes import generic
from venues.models._common import CommonModel

__author__ = 'm'


class Review(CommonModel):
    '''
    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')

    rating = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    @staticmethod
    def list_for_venue(venue):
        related_object_type = ContentType.objects.get_for_model(venue)
        return Review.objects.filter(content_type__pk=related_object_type.id,
                                      venue_id=venue.id)

    @property
    def venue_name(self):
        return self.content_object.name

    def __unicode__(self):
        return self.text[:25]

    @property
    def short_text(self):
        return self.__unicode__()
