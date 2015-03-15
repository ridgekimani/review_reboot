from django.contrib.contenttypes.models import ContentType
from venues.models import Note
from venues.models.restaurant import Restaurant
from venues.tests import TestCaseVenue

__author__ = 'm'


class TestNotes(TestCaseVenue):

    def test_guest_cant_remove_note(self):
        note = Note.objects.create(content_type_id=0, venue_id=0)
        self.redirect_to_login_on_get("venues.views.notes.remove_note", pargs=[note.pk])
        self.assertEqual(1, Note.objects.filter(pk=note.pk).count())

    @TestCaseVenue.login
    def test_user_can_delete_his_notes(self):
        note = Note.objects.create(content_type_id=0, venue_id=0, created_by=self.user)
        self.redirect_on_get("venues.views.notes.remove_note", pargs=[note.pk])
        self.assertEqual(0, Note.objects.filter(pk=note.pk).count())

    @TestCaseVenue.login
    def test_user_CANT_delete_NOT_his_notes(self):
        note = Note.objects.create(content_type_id=0, venue_id=0)
        self.redirect_to_login_on_get("venues.views.notes.remove_note", pargs=[note.pk])
        self.assertEqual(Note.objects.filter(pk=note.pk).count(), 1)

    @TestCaseVenue.moderator
    def test_moderator_CAN_delete_any_notes(self):
        note = Note.objects.create(content_type_id=0, venue_id=0)
        self.redirect_on_get("venues.views.notes.remove_note", pargs=[note.pk])
        self.assertEqual(Note.objects.filter(pk=note.pk).count(), 0)

    @TestCaseVenue.superuser
    def test_superuser_CAN_delete_any_notes(self):
        note = Note.objects.create(created_by=self.user, content_type_id=0, venue_id=0)
        self.redirect_on_get("venues.views.notes.remove_note", pargs=[note.pk])
        self.assertEqual(Note.objects.filter(pk=note.pk).count(), 0)

    def test_guest_cant_add_notes(self):
        r = Restaurant(name='ajskdajsdas')
        r.save()
        self.redirect_to_login_on_post("venues.views.notes.add_note", pargs=[r.pk])

    @TestCaseVenue.login
    def test_user_can_add_notes(self):
        r = Restaurant(name='ajskdajsdas', approved=True)
        r.save()
        params = {
            'text': 'a;lsdlasdlaksnd,mxnckajsldasdsometext'
        }
        self.redirect_on_post("venues.views.notes.add_note", pargs=[r.pk], params=params)
        note = Note.objects.filter(venue_id=r.id).order_by('-pk').first()
        self.assertEqual(note.text, params['text'])

    @TestCaseVenue.login
    def test_user_cant_add_notes_to_notapproved_restaurant(self):
        r = Restaurant(name='ajskdajsdas')
        r.save()
        params = {
            'text': 'a;lsdlasdlaksnd,mxnckajsldakjashdkjasdsdsometext'
        }
        self.redirect_to_login_on_post("venues.views.notes.add_note", pargs=[r.pk], params=params)

    @TestCaseVenue.moderator
    def test_moderator_can_add_notes(self):
        r = Restaurant(name='ajskdajsdas')
        r.save()
        params = {
            'text': 'a;lsdlasdlaksnd,mxnckajsldasdsometext'
        }
        self.redirect_on_post("venues.views.notes.add_note", pargs=[r.pk], params=params)
        note = Note.objects.filter(venue_id=r.id).order_by('-pk').first()
        self.assertEqual(note.text, params['text'])

    @TestCaseVenue.superuser
    def test_superuser_can_add_notes(self):
        r = Restaurant(name='ajskdajsdas')
        r.save()
        params = {
            'text': 'a;lsdlasdlaksnd,mxnckajsldasdsometext'
        }
        self.redirect_on_post("venues.views.notes.add_note", pargs=[r.pk], params=params)
        note = Note.objects.filter(venue_id=r.id).order_by('-pk').first()
        self.assertEqual(note.text, params['text'])

    def test_guest_cant_update_note(self):
        note = Note.objects.create(content_type_id=0, venue_id=0)
        self.redirect_to_login_on_post("venues.views.notes.update_note", pargs=[note.pk],)
        self.redirect_to_login_on_get("venues.views.notes.update_note", pargs=[note.pk],)

    @TestCaseVenue.login
    def test_user_can_update_his_note(self):
        r = Restaurant(name="jaksjdaklsd", approved=True)
        r.save()
        note = Note.objects.create(content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                   venue_id=r.id, created_by=self.user)

        params = {
            'text': 'new_text'
        }

        self.can_get("venues.views.notes.update_note", pargs=[note.pk])
        self.redirect_on_post("venues.views.notes.update_note", pargs=[note.pk], params=params)
        note = Note.objects.get(pk=note.pk)
        self.assertEqual(note.text, params['text'])

    @TestCaseVenue.login
    def test_user_CANT_update_not_his_note(self):
        r = Restaurant(name="jaksjdaklsd")
        r.save()
        note = Note.objects.create(content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                   venue_id=r.id, created_by=self.user)

        params = {
            'text': 'new_text'
        }

        self.redirect_to_login_on_get("venues.views.notes.update_note", pargs=[note.pk])
        self.redirect_to_login_on_post("venues.views.notes.update_note", pargs=[note.pk], params=params)

    @TestCaseVenue.moderator
    def test_moderator_can_update_note(self):
        r = Restaurant(name="jaksjdaklsd")
        r.save()
        note = Note.objects.create(content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                   venue_id=r.id, created_by=self.user)

        params = {
            'text': 'new_text'
        }

        self.can_get("venues.views.notes.update_note", pargs=[note.pk])
        self.redirect_on_post("venues.views.notes.update_note", pargs=[note.pk], params=params)
        note = Note.objects.get(pk=note.pk)
        self.assertEqual(note.text, params['text'])

    @TestCaseVenue.superuser
    def test_superuser_can_update_note(self):
        r = Restaurant(name="jaksjdaklsd")
        r.save()
        note = Note.objects.create(content_type_id=ContentType.objects.get_for_model(Restaurant).id,
                                   venue_id=r.id, created_by=self.user)

        params = {
            'text': 'new_text'
        }

        self.can_get("venues.views.notes.update_note", pargs=[note.pk])
        self.redirect_on_post("venues.views.notes.update_note", pargs=[note.pk], params=params)
        note = Note.objects.get(pk=note.pk)
        self.assertEqual(note.text, params['text'])

    def test_anyone_can_get_show_all_notes(self):
        r = Restaurant(name="jkasdhaksd")
        r.save()
        n = Note.objects.create(venue_id=r.id, content_type_id=ContentType.objects.get_for_model(Restaurant).id, text='LKJaklsjdasd')
        response = self.can_get("venues.views.notes.show_all_notes", pargs=[r.id])
        self.assertContains(response, n.text)
