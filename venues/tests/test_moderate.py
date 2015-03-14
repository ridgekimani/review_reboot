from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from restaurant.utils import TestCaseEx
from venues.models import Restaurant
from venues.models.report import Report
from venues.models.review import Review
from venues.tests import TestCaseVenue


class TestModerate(TestCaseVenue):
    def test_guest_cant_access_index_page(self):
        self.redirect_to_login_on_get("venues.views.moderate.index")

    @TestCaseEx.login
    def test_simpler_user_cant_access_index_page(self):
        self.redirect_to_login_on_get("venues.views.moderate.index")

    @TestCaseVenue.moderator
    def test_moderator_CAN_access_index_page(self):
        self.can_get("venues.views.moderate.index")

    @TestCaseEx.superuser
    def test_superuser_CAN_access_index_page(self):
        self.can_get("venues.views.moderate.index")

    @TestCaseEx.login
    def test_simpler_user_cant_access_reports_page(self):
        self.redirect_to_login_on_get("venues.views.moderate.reports")

    @TestCaseVenue.moderator
    def test_moderator_CAN_access_reports_page(self):
        self.can_get("venues.views.moderate.reports")

    @TestCaseEx.superuser
    def test_superuser_CAN_access_reports_page(self):
        self.can_get("venues.views.moderate.reports")

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
        rest = Restaurant.objects.get(pk=rest.pk)
        self.assertEqual(rest.approved, False)

    @TestCaseVenue.moderator
    def test_moderator_can_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        self.redirect_on_post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])
        rest = Restaurant.objects.get(pk=rest.pk)
        self.assertEqual(rest.approved, True)

    @TestCaseEx.superuser
    def test_superuser_can_approve_restaurant(self):
        rest = Restaurant(
            name="1244",
            address="245",
            phone="1923819273",
        )
        rest.save()

        self.redirect_on_post("venues.views.moderate.approve_restaurant", params={'approved': True}, pargs=[
            rest.pk
        ])

        rest = Restaurant.objects.get(pk=rest.pk)
        self.assertEqual(rest.approved, True)

    def test_guest_cant_approve_review(self):
        review = Review.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        review.approved = False
        review.save()
        self.redirect_to_login_on_get("venues.views.moderate.approve_review", params={'approved': True}, pargs=[
            review.pk
        ])

        review = Review.objects.get(id=review.id)
        self.assertEqual(review.approved, False)

    @TestCaseEx.login
    def test_simple_user_cant_approve_review(self):
        review = Review.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        review.approved = False
        review.save()
        self.redirect_to_login_on_get("venues.views.moderate.approve_review", params={'approved': True}, pargs=[
            review.pk
        ])

        review = Review.objects.get(id=review.id)
        self.assertEqual(review.approved, False)

    @TestCaseVenue.moderator
    def test_moderator_can_approve_review(self):
        review = Review.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        review.approved = False
        review.save()
        self.redirect_on_get("venues.views.moderate.approve_review", params={'approved': True}, pargs=[
            review.pk
        ])

        review = Review.objects.get(id=review.id)
        self.assertEqual(review.approved, True)

    @TestCaseVenue.superuser
    def test_superuser_can_approve_review(self):
        review = Review.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        review.approved = False
        review.save()
        self.redirect_on_get("venues.views.moderate.approve_review", params={'approved': True}, pargs=[
            review.pk
        ])

        review = Review.objects.get(id=review.id)
        self.assertEqual(review.approved, True)


    def test_guest_cant_resolve_report(self):
        report = Report.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        report.resolved = False
        report.save()
        self.redirect_to_login_on_get("venues.views.moderate.resolve_report", params={'approved': True}, pargs=[
            report.pk
        ])

        report = Report.objects.get(id=report.id)
        self.assertEqual(report.resolved, False)

    @TestCaseEx.login
    def test_simpleuser_cant_resolve_report(self):
        report = Report.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        report.resolved = False
        report.save()
        self.redirect_to_login_on_get("venues.views.moderate.resolve_report", params={
            'approved': True
        }, pargs=[
            report.pk
        ])

        report = Report.objects.get(id=report.id)
        self.assertEqual(report.resolved, False)

    @TestCaseVenue.moderator
    def test_moderator_can_resolve_report(self):
        report = Report.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        report.resolved = False
        report.save()

        params = {
            'approved': True,
            'moderator_note': 'alshdashdkashmdoashd'
        }

        self.redirect_on_post("venues.views.moderate.resolve_report", params=params, pargs=[
            report.pk
        ])

        report = Report.objects.get(id=report.id)

        self.assertEqual(report.resolved, True)
        self.assertEqual(report.moderator_note, params['moderator_note'])
        self.assertEqual(report.closed_by, self.moderator)

    @TestCaseVenue.superuser
    def test_superuser_can_resolve_report(self):
        report = Report.objects.create(
            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
            venue_id=0
        )
        report.resolved = False
        report.save()

        params = {
            'approved': True,
            'moderator_note': 'alshdashdkashmdoashd'
        }

        self.redirect_on_post("venues.views.moderate.resolve_report", params=params, pargs=[
            report.pk
        ])

        report = Report.objects.get(id=report.id)

        self.assertEqual(report.resolved, True)
        self.assertEqual(report.moderator_note, params['moderator_note'])
        self.assertEqual(report.closed_by, self.root)
