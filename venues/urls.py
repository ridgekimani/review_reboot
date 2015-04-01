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
    url(r'profile/approved/$', 'profile.approvedrestaurants'),
    url(r'profile/updated/$', 'profile.updated_restaurants'),
    url(r'profile/$', 'profile.myprofile'),
    url(r'user/(?P<pk>.+)/profile/$', 'profile.user_profile'),
    url(r'user/(?P<pk>.+)/profile/form/$', ProfileUpdateView.as_view(), name='profile-form'),

    # venues
    url(r'restaurant/(?P<rest_pk>[0-9]+)/show-all-reviews/$', 'reviews.show_all_reviews'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/show-all-tips/$', 'notes.show_all_notes'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/report/$', 'reports.report_restaurant'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/update/$', 'venuess.update_restaurant'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/approve/$', 'moderate.approve_restaurant'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/$', 'venuess.restaurant', name="restaurant_profile"),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/note/new/$', 'notes.add_note'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/review/new/$', 'reviews.add_review'),

    url(r'restaurant/(?P<rest_pk>[0-9]+)/writereview/$', 'venuess.add_review_view', name='restaurant_writereview'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/addnote/$', 'venuess.add_note_view', name='restaurant_addnote'),

    url(r'restaurant/(?P<rest_pk>[0-9]+)/moderate/$', 'moderate.moderate_restaurant'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/unsuspend/$', 'moderate.unsuspend_restaurant'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/remove/$', 'moderate.suspend_restaurant'),

    url(r'restaurant/(?P<rest_pk>[0-9]+)/allreviews/$', 'venuess.all_reviews_view', name='restaurant_allreviews'),
    url(r'restaurant/(?P<rest_pk>[0-9]+)/allnotes/$', 'venuess.all_notes_view', name='restaurant_allnotes'),

    # common
    url(r'get_category/', 'get_category', name='get_drugs'),
    url(r'new/$', 'venuess.add_restaurant', name='add_restaurant'),

    #search
    #url(r'search/', 'venuess.search_view', name='search'),

    # restautant by slug
    url(r'(?P<slug>[\w-]+)/$', 'venuess.restaurant_by_slug'),
    # index page
    url(r'$', 'venuess.index', name='index'),
)
