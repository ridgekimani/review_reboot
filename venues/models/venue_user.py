from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


User.add_to_class("is_venue_moderator", lambda self: self.venue_moderator if hasattr(self, "venue_moderator") and self.venue_moderator else self.is_superuser)

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