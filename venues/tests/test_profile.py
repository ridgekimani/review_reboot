from django.contrib.contenttypes.models import ContentType
from venues.models.note import Note
from venues.models.report import Report
from venues.models.restaurant import Restaurant
from venues.models.review import Review
from venues.tests import TestCaseVenue

__author__ = 'm'


class TestProfile(TestCaseVenue):
    def setUp(self):
        super(TestProfile, self).setUp()

        self.userRestaurant = Restaurant(name="lkajhsdklahsdkjasd", created_by=self.user)
        self.userRestaurant.save()
        self.alienRestaurant = Restaurant(name="lkahsdjashdkansdmnm")
        self.alienRestaurant.save()

        self.userNote1 = Note.objects.create(text="kashdkjashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.userRestaurant.id)
        self.userNote2 = Note.objects.create(text="kashdkjasdasdashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)
        self.alienNote = Note.objects.create(text="kashdkjasdasfasddashdas",
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)

        self.userReview1 = Review.objects.create(text="kashdkjashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.userRestaurant.id)
        self.userReview2 = Review.objects.create(text="kashdkjasdasdashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)
        self.alienReview = Review.objects.create(text="kashdkjasdasasdasdashdas",
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)

        self.userReport1 = Report.objects.create(note="kashdkjashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.userRestaurant.id)
        self.userReport2 = Report.objects.create(note="kashdkjasdasdashdas", created_by=self.user,
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)
        self.alienReport = Report.objects.create(note="kashdkjasdaasdasdsdashdas",
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.alienRestaurant.id)

    def test_guest_cant_view_profile_pages(self):
        self.redirect_to_login_on_get("venues.views.profile.myrestaurants")
        self.redirect_to_login_on_get("venues.views.profile.myreviews")
        self.redirect_to_login_on_get("venues.views.profile.mynotes")
        self.redirect_to_login_on_get("venues.views.profile.myreports")

    @TestCaseVenue.login
    def test_user_can_view_his_restaurants(self):
        response = self.can_get("venues.views.profile.myrestaurants")
        self.assertContains(response, self.userRestaurant.name)
        self.assertNotContains(response, self.alienRestaurant.name)

    @TestCaseVenue.login
    def test_user_can_view_his_notes(self):
        response = self.can_get("venues.views.profile.mynotes")
        self.assertContains(response, self.userNote1.text)
        self.assertContains(response, self.userNote2.text)
        self.assertNotContains(response, self.alienNote.text)

    @TestCaseVenue.login
    def test_user_can_view_his_reviews(self):
        response = self.can_get("venues.views.profile.myreviews")
        self.assertContains(response, self.userReview1.text)
        self.assertContains(response, self.userReview2.text)
        self.assertNotContains(response, self.alienReview.text)

    @TestCaseVenue.login
    def test_user_can_view_his_reports(self):
        response = self.can_get("venues.views.profile.myreports")
        self.assertContains(response, self.userReport1.note)
        self.assertContains(response, self.userReport2.note)
        self.assertNotContains(response, self.alienReport.note)


