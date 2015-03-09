from django.conf.urls import url, patterns
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = patterns('venues.views',
    url(r'notes/(?P<note_pk>[0-9]+)/remove/$', 'notes.remove_note'),
    url(r'notes/(?P<note_pk>[0-9]+)/update/$', 'notes.update_note'),

    url(r'comments/(?P<comment_pk>[0-9]+)/remove/$', 'comments.remove_comment'),
    url(r'comments/(?P<comment_pk>[0-9]+)/update/$', 'comments.update_comment'),

    url(r'moderate/$', 'moderate.index'),

    url(r'(?P<rest_pk>[0-9]+)/show-all-comments/$', 'comments.show_all_comments'),
    url(r'(?P<rest_pk>[0-9]+)/show-all-tips/$', 'notes.show_all_notes'),
    url(r'(?P<rest_pk>[0-9]+)/report/$', 'reports.report_restaurant'),

    url(r'(?P<rest_pk>[0-9]+)/update/$', 'venuess.update_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/approve/(?P<approve>0|1)$', 'venuess.approve_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/profile$', 'venuess.restaurant'),
    url(r'new$', 'venuess.add_restaurant'),

    url(r'(?P<rest_pk>[0-9]+)/note/new/$', 'notes.add_note'),

    url(r'(?P<rest_pk>[0-9]+)/comment/new/', 'comments.add_comment'),
    url(r'(?P<rest_pk>[0-9]+)/comment/$', 'comments.comment'),

    url(r'restaurants_lists/$', 'venuess.restaurants_lists'),
    url(r'get_category/', 'get_category', name='get_drugs'),

    url(r'(?P<slug>[\w-]+)/$', 'venuess.restaurant_by_slug'),
)