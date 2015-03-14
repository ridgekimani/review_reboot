from django.contrib.auth.models import User
from restaurant.utils import TestCaseEx
from venues.models import Restaurant


class TestVenuess(TestCaseEx):
    def test_guest_cant_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        response = self.post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])
        self.assertEqual(response.status_code, 302)

    @TestCaseEx.login
    def test_simple_user_cant_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        response = self.post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])
        self.assertEqual(response.status_code, 302)

    def test_moderator_can_approve_restaurant(self):
        user = User.objects.create_user("temp", password="123")
        user.venueuser.venue_moderator = True
        user.venueuser.save()

        self.client.login(username=user.username, password="123")
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        self.can_post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])
        self.client.logout()

    @TestCaseEx.superuser
    def test_superuser_can_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        self.can_post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])
