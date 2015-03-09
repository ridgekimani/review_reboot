from restaurant.utils import TestCaseEx
from venues.models import Restaurant


class TestVenuess(TestCaseEx):
    def test_guest_cant_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
            cuisine="asdkasdl",
        )
        rest.save()

        self.post("venues.views.venuess.approve_restaurant", pargs=[
            rest.pk, 1
        ])

    @TestCaseEx.login
    def test_simple_user_cant_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
            cuisine="asdkasdl",
        )
        rest.save()

        self.post("venues.views.venuess.approve_restaurant", pargs=[
            rest.pk, 1
        ])

    def test_moderator_can_approve_restaurant(self):
        pass

    def test_superuser_can_approve_restaurant(self):
        pass