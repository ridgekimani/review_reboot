from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


def is_venue_moderator(user):
    if hasattr(user, "venueuser"):
        return user.is_superuser or user.venue_user.venue_moderator
    else:
        return user.is_superuser

User.add_to_class("is_venue_moderator", is_venue_moderator)
User.venue_user = property(lambda u: VenueUser.objects.get_or_create(user=u)[0])


class VenueUser(models.Model):
    user = models.OneToOneField(User)
    venue_moderator = models.BooleanField(default=False,
                                          help_text="Is user can approve, remove, and see not approved venues")


# signal for creating venue_user info for each new user
def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = VenueUser(user=user, venue_moderator=user.is_superuser)
        up.save()


post_save.connect(create_profile, sender=User)