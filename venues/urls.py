from django.conf.urls import url, patterns
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = patterns('venues.views',
    url(r'notes/(?P<note_pk>[0-9]+)/remove/', 'remove_note'),
    url(r'notes/(?P<note_pk>[0-9]+)/update/', 'update_note'),
    # url(r'notes/(?P<note_pk>[0-9]+)/', 'note'),

    url(r'(?P<rest_pk>[0-9]+)/show-all-comments/$', 'show_all_comments'),
    url(r'(?P<rest_pk>[0-9]+)/show-all-tips/$', 'show_all_tips'),
    url(r'(?P<rest_pk>[0-9]+)/report/$', 'report_restaurant'),

    url(r'(?P<rest_pk>[0-9]+)/update/$', 'update_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/profile$', 'restaurant'),

    url(r'(?P<rest_pk>[0-9]+)/note/new/$', 'add_note'),

    url(r'(?P<rest_pk>[0-9]+)/comment/new/', 'add_comment'),
    url(r'(?P<rest_pk>[0-9]+)/comment/$', 'comment'),

    url(r'restaurants_lists/$', 'restaurants_lists'),
    url(r'get_category/', 'get_category', name='get_drugs'),

    url(r'(?P<slug>[\w-]+)/$', 'restaurant_by_slug'),
)