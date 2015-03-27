from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class CommonModel(Model):
    """
    this is common model for all models, which in tandem with CommonForm
    allows to track user, modification date and modification ip
    """
    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created_by",
                                   default=None, null=True, blank=True, editable=False)

    created_by_ip = models.CharField(blank=True, max_length=30)

    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="%(class)s_modified_by",
                                   default=None, null=True, blank=True, editable=False)

    modified_ip = models.CharField(default='', max_length=39, editable=False)
