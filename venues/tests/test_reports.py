from django.contrib.contenttypes.models import ContentType
from venues.models.report import Report
from venues.models.restaurant import Restaurant
from venues.tests import TestCaseVenue

__author__ = 'm'


class TestReports(TestCaseVenue):

    def setUp(self):
        super(TestReports, self).setUp()
        self.restaurant = Restaurant(name="lashdkjasd")
        self.restaurant.save()

        self.report = Report.objects.create(note="kjashda",
                                            content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                            venue_id=self.restaurant.id)

    def test_guest_cant_report_restaurant(self):
        self.redirect_to_login_on_get("venues.views.reports.report_restaurant", pargs=[self.restaurant.id])

    @TestCaseVenue.login
    def test_login_user_CAN_report_restaurant(self):
        Report.objects.all().delete()

        params = {
            'type': 1,
            'note': 'alksjdlkasjd'
        }

        self.can_get("venues.views.reports.report_restaurant", pargs=[self.restaurant.id])
        self.redirect_on_post("venues.views.reports.report_restaurant", pargs=[self.restaurant.id], params=params)

        self.assertEqual(Report.objects.filter(**params).count(), 1)

    def test_guest_cant_moderate(self):
        self.redirect_to_login_on_get("venues.views.reports.moderate_reports")

    @TestCaseVenue.login
    def test_simple_user_cant_moderate(self):
        self.redirect_to_login_on_get("venues.views.reports.moderate_reports")

    @TestCaseVenue.moderator
    def test_moderator_can_moderate(self):
        self.can_get("venues.views.reports.moderate_reports")

    @TestCaseVenue.superuser
    def test_superuser_can_moderate(self):
        self.can_get("venues.views.reports.moderate_reports")

    def test_guest_cant_moderate_report(self):
        self.redirect_to_login_on_get("venues.views.reports.moderate_report", pargs=[self.report.id,])

    @TestCaseVenue.login
    def test_simple_user_cant_moderate_report(self):
        self.redirect_to_login_on_get("venues.views.reports.moderate_report", pargs=[self.report.id,])

    @TestCaseVenue.moderator
    def test_moderator_CAN_moderate_report(self):
        params = {
            "resolved": True,
            "moderator_note": 'alskkdlaksjdlkasd'
        }
        self.redirect_on_post("venues.views.reports.moderate_report", pargs=[self.report.id,], params=params)

        self.report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(self.report.moderator_note, params['moderator_note'])
        self.assertEqual(self.report.resolved, params['resolved'])
