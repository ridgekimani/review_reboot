from django.contrib.contenttypes.models import ContentType
from venues.models.restaurant import Restaurant
from venues.models.review import Review
from venues.tests import TestCaseVenue

__author__ = 'm'

class TestReviews(TestCaseVenue):

    def test_anyone_can_get_show_all_reviews(self):
        rest = Restaurant(name="kajshdkjasdas")
        rest.save()
        self.can_get("venues.views.reviews.show_all_reviews", pargs=[rest.pk])

    # def test_guest_cant_remove_review(self):
    #     self.userReview1 = Review.objects.create(text="kashdkjashdas", created_by=self.user,
    #                                         content_type_id=ContentType.objects.get_for_model(Restaurant).id,
    #                                         venue_id=self.userRestaurant.id)
