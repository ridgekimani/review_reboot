from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class VenueUser(models.Model):
    user = models.OneToOneField(User)
    venue_moderator = models.BooleanField(default=False,
                                          help_text="Is user can approve, remove, and see not approved venues")

    @property
    def is_venue_moderator(self):
        """
        :return: True if user can moderate
        """
        return self.venue_moderator or self.user.is_superuser


# signal for creating venue_user info for each new user
def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = VenueUser(user=user, venue_moderator=user.is_superuser)
        up.save()
post_save.connect(create_profile, sender=User)