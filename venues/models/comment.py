from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes import generic

__author__ = 'm'

class Comment(models.Model):
    '''
    This class uses generic ForeignKey, for details read here
    https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations
    '''
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, editable=False)
    venue_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'venue_id')
    rating = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)

    modified_ip = models.CharField(default='', max_length=39, editable=False)

    @staticmethod
    def list_for_venue(venue):
        related_object_type = ContentType.objects.get_for_model(venue)
        return Comment.objects.filter(content_type__pk=related_object_type.id,
                                      venue_id=venue.id)

    @property
    def venue_name(self):
        return self.content_object.name

    def __unicode__(self):
        return self.text[:25]

    @property
    def short_text(self):
        return self.__unicode__()
