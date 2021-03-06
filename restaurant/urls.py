from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.views.generic import TemplateView
import venues.urls
import venues.views
import venues.views.reports
import venues.views.venuess

admin.autodiscover()


urlpatterns = patterns('',


    url(r'^moderate-reports/$', venues.views.reports.moderate_reports),
    url(r'^reports/(?P<pk>[0-9]+)/moderate/$', venues.views.reports.moderate_report),

    #python-social-login urls
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    # url(r'^register-by-token/(?P<backend>[^/]+)/$', venues.views.register_by_access_token),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="account_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="account_logout"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include(venues.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )