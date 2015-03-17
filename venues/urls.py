from django.conf.urls import url, patterns
from django.conf.urls.i18n import i18n_patterns
from venues.views.profile import ProfileUpdateView

__author__ = 'm'

urlpatterns = patterns('venues.views',
    # notes editing
    url(r'notes/(?P<note_pk>[0-9]+)/remove/$', 'notes.remove_note'),
    url(r'notes/(?P<note_pk>[0-9]+)/update/$', 'notes.update_note'),

    # reviews editing
    url(r'reviews/(?P<review_pk>[0-9]+)/remove/$', 'reviews.remove_review'),
    url(r'reviews/(?P<review_pk>[0-9]+)/update/$', 'reviews.update_review'),
    url(r'reviews/(?P<review_pk>[0-9]+)/approve/$', 'moderate.approve_review'),

    # moderate
    url(r'moderate/$', 'moderate.index'),
    url(r'moderate/reports$', 'moderate.reports'),
    url(r'moderate/reports/(?P<id>[0-9]+)/close$', 'moderate.resolve_report'),

    #profile
    url(r'profile/restaurants/$', 'profile.myrestaurants'),
    url(r'profile/reviews/$', 'profile.myreviews'),
    url(r'profile/notes/$', 'profile.mynotes'),
    url(r'profile/reports/$', 'profile.myreports'),
    url(r'profile/$', 'profile.myprofile'),
    url(r'profile/form/(?P<pk>.+)/$', ProfileUpdateView.as_view(), name='profile-form'),

    # venues
    url(r'(?P<rest_pk>[0-9]+)/show-all-reviews/$', 'reviews.show_all_reviews'),
    url(r'(?P<rest_pk>[0-9]+)/show-all-tips/$', 'notes.show_all_notes'),
    url(r'(?P<rest_pk>[0-9]+)/report/$', 'reports.report_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/remove', 'venuess.remove_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/update/$', 'venuess.update_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/approve/$', 'moderate.approve_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/profile$', 'venuess.restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/note/new/$', 'notes.add_note'),
    url(r'(?P<rest_pk>[0-9]+)/review/new/', 'reviews.add_review'),
    url(r'(?P<rest_pk>[0-9]+)/review/$', 'reviews.review'),

    # common
    url(r'get_category/', 'get_category', name='get_drugs'),
    url(r'new$', 'venuess.add_restaurant'),

    # restautant by slug
    url(r'(?P<slug>[\w-]+)/$', 'venuess.restaurant_by_slug'),
    # index page
    url(r'$', 'venuess.index'),
)
