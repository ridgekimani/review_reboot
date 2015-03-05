from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.views.generic import TemplateView

import venues.views as views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'restaurant.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^restaurants/restaurants_lists/$', views.restaurants_lists),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/comment/$', views.comment),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/show-all-comments/$', views.show_all_comments),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/tip/$', views.tip),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/show-all-tips/$', views.show_all_tips),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/update/$', views.update_restaurant),
    url(r'^restaurants/(?P<rest_pk>[0-9]+)/report/$', views.report_restaurant),
    url(r'^moderate-reports/$', views.moderate_reports),
    url(r'^reports/(?P<pk>[0-9]+)/moderate/$', views.moderate_report),
    url(r'^restaurants/get_category/', views.get_category, name='get_drugs'),

    #python-social-login urls
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register-by-token/(?P<backend>[^/]+)/$', views.register_by_access_token),

    # pinax accounts urls
    url(r"^owner/$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^owner/account/", include("account.urls")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.closest),

    # url(r'^logout/$', views.log_out),
)

