from django.contrib.auth.models import User
from restaurant.utils import TestCaseEx

__author__ = 'm'


class TestCaseVenue(TestCaseEx):
    def setUp(self):
        self.moderator = User.objects.create_user("moderator", "", "")
        self.moderator.venueuser.venue_moderator = True
        self.moderator.venueuser.save()

        super(TestCaseVenue, self).setUp()

    @staticmethod
    def moderator(fn, user=None):
        def _wrapper(self=None):
            if user:
                self.client.login(username=self.moderator.username, password="")
            else:
                self.client.login(username=self.moderator.username, password="")
            fn(self)
            self.client.logout()

        return _wrapper
